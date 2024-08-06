from __future__ import annotations

from typing import Callable, Annotated
from functools import wraps
import time
import logging
import threading
from pydantic import (PositiveFloat, NonNegativeFloat, Field, validate_call,
    PositiveInt)

import statistics 
from astropy.time import Time, TimeDelta

from .types import TimeType, TimeDeltaType

StrictFraction: type = Annotated[float, Field(gt=0, lt=1)]
Direction: type = Annotated[int, Field(ge=-1, le=1)]

def seconds_in_day(t: TimeType):
    """Number of seconds in a day

Arguments
    t [astropy.time.Time]:
        Time
    """        
    if t.scale != 'utc':
        return 86_400
    
    mjd1 = int(t.mjd)
    start_of_today = Time(mjd1, format='mjd') 
    start_of_tomorrow = Time(mjd1 + 1, format='mjd') 
    sec_in_day = (start_of_tomorrow - start_of_today).sec

    return sec_in_day

@validate_call
def round(t: TimeType, interval: TimeDeltaType = '1s', *, dir: Direction = 0):
    """round a time to a given precision

If normal days (i.e. not leap days) can be exactly be devided in intervals 
of length interval, the routine performs high precision calculations, to 
limit rounding errors and properly deal with possible leap/drop seconds.

Otherwise, the rounding occurs as a rounding of the MJD date.

Arguments
    t [astropy.time.Time]:
        Time

    interval [astropy.time.TimeDelta]:
        Time interval indicating the precision of the rounding

    direction [int]:
        Direction of the rounding (-1: lower, +1: upper, 0: nearest)        

    """ 
    scale = t.scale
    i_sec = interval.sec
    high_precision = 86_400 % i_sec

    if not high_precision:
        # i_day should be a integer number of days or a fraction of
        # days (e.g. 1.5, 4/3) if the rounding needs to make sense.
        mjd = t.mjd
        i_day = i_sec / 86_400
        r_day = (mjd % i_day)
        if dir == 0:
            dir = -1 if r_day < i_day / 2 else 1
        mjd_rounded = mjd - r_day + (i_day if dir > 0 else 0)
        t_rounded = Time(mjd_rounded, format='mjd', scale=scale) 

        return t_rounded

    # Time has no "second of the day" routine, so we'll do it using MJD.  
    # MJD are stretched on leap days, they are 86400 or 86401 s long. 

    sec_in_day = seconds_in_day(t)
    mjd1 = t.jd1 - 2_400_001    
    mjd2 = t.jd2 + 0.5
    sod = mjd2 * sec_in_day
    
    r_sec = sod % i_sec
    if dir == 0:
        dir = -1 if r_sec < i_sec / 2 else 1

    rounded_sod = sod - r_sec
    if dir > 0:
        rounded_sod += i_sec
        # because of rounding errors and leap seconds we can't just test 
        # whether the  rounded limit is exactly on the new day. Instead,
        # let's look wether the next interval would fit in the
        # present day within rounding errors
        epsilon = 1e-5
        if rounded_sod + i_sec > sec_in_day + epsilon * i_sec:
            rounded_sod = 0
            mjd1 += 1

    mjd2_rounded = rounded_sod / sec_in_day
    t_rounded = Time(mjd1, mjd2_rounded, format='mjd', scale=scale)

    return t_rounded.to_value(t.format)
 
def ceil(t: TimeType, interval: TimeDeltaType = '1s'):
    """round a time to a given precision

If normal days (i.e. not leap days) can be exactly be devided in intervals 
of length interval, the routine performs high precision calculations, to 
limit rounding errors and properly deal with possible leap/drop seconds.

Otherwise, the rounding occurs as a rounding of the MJD date.

Arguments
    t [astropy.time.Time]:
        Time

    interval [astropy.time.TimeDelta]:
        Time interval indicating the precision of the rounding

    """ 
    return round(t, interval, dir=1)
   
def floor(t: TimeType, interval: TimeDeltaType = '1s'):
    """truncate a time to a given precision

If normal days (i.e. not leap days) can be exactly be devided in intervals 
of length interval, the routine performs high precision calculations to 
limit rounding errors.

Otherwise, the rounding occurs as a truncation of the MJD date.

Arguments
    t [astropy.time.Time]:
        Time

    interval [astropy.time.TimeDelta]:
        Time interval indicating the precision of the rounding

    """ 
    return round(t, interval, dir=-1)
 
@validate_call
def average(
        *,
        interval: TimeDeltaType,
        sampling: TimeDeltaType,
        sampling_dir: Direction = 0,
        initial_delay: TimeDeltaType = '0.1s',
        sync: str | None = None,
        averaging_fun: Callable = statistics.mean,
        sleep_overhead: NonNegativeFloat = 1e-3,
        sleep_fraction: StrictFraction = 0.6,
):
    """Average value of a function taken at regular time intervals

Example:

    @average(interval='5min', sampling='15s', sync='utc', sampling_dir=1)
    def f(...) -> float:
        ...

    Will define a function that returns a 5 min average of f(...) sampled
    every 15s synchronised with UCT, i.e. on intervals [00:00:00 - 00:05:00],
    [00:05:00 - 00:10:00] etc. with sampling performed at 00:00:15 ... 00:05:00
    on the first interval.

Keyword arguments:

    interval [TimeDelta]: 
        Averaging interval

    sampling [TimeDelta]:
        Function is evaluated every sampling

    sampling_dir [-1, 0, 1, default: 0]:
        Wether sampling occurs at the start, middle, or end of an interval.

    initial_delay [TimeDelta, default: '0.1s']:
        Initial delay before first interval starts.

    sync [str, default: None]:
        If True, the interval and sampling follow timescale 'sync'
        (e.g. UTC or TAI). 
        
        For instance, with sync='utc', interval='1min', sampling='5s', 
        the interval ends at the end of the current UCT minute and sampling 
        occurs at seconds 2.5, 12.5, ..., 57.5.  (Obviously, the times
        already ellapsed are not sampled.) 

    averaging_fun
        A callable that can average a list of results of fun.

    sleep_fraction [float]
        Once the function has finished its periodic call sleep for a 
        fraction of the remaining time to avoid saturating the processor.

    sleep_overhead [float, s]
        Maximum overheads associated with the sleep loop.  Depends on CPU speed
        and load, YMMV.

""" 
    def decorator(f):
        
        @wraps(f)
        def wrapper(*args, **kwargs):
          
            # determine the end of the interval
            now = Time(Time.now(), scale=sync) + initial_delay
            offset = sampling / 2 * (1 + sampling_dir)
            if sync:
                end = ceil(now, interval) 
                start = ceil(now - offset, sampling) + sampling 
            else:
                end = now + interval
                start = now  

            n_samples = int(((end - start) / sampling).value + 0.5)
            t_target = start + offset
            max_overshoot = interval.sec / 10
            results = [] 

            for i in range(n_samples):
                overshoot = sleep_until(
                    t_target.unix,
                    sleep_overhead=sleep_overhead,
                    sleep_fraction=sleep_fraction,
                )
                if overshoot > max_overshoot:
                    continue
                results.append(f(*args, **kwargs))
                t_target += sampling
           
            return averaging_fun(results)

        return wrapper

    return decorator 

def cached_method(
        fun: Callable | None = None,
        *,
        expire_after: PositiveFloat = 4.35e+17
):

    def decorator(f):
        
        @wraps(f)
        def wrapper(obj, *args, **kwargs):
         
            key = args, tuple(kwargs.items())
 
            with wrapper.lock: 

                last_update, last_result = wrapper.cache.get(key, (0, None))
                
                if time.time() - last_update > expire_after:
                    last_result = f(obj, *args)
                    last_update = time.time()
                    wrapper.cache[key] = (last_update, last_result)
                
            return last_result

        wrapper.cache = {}
        wrapper.lock = threading.Lock()

        return wrapper

    return decorator if fun is None else decorator(f)

def sleep(
        dt: PositiveFloat,
        sleep_overhead: NonNegativeFloat = 1e-3,
        sleep_fraction: StrictFraction = 0.6,
):
    """
Semi-precise sleep function with about microsond accuracy.
 
Arguments

    dt [float, s]: 
        Time interval. 

Optional keyword arguments:

    sleep_overhead [float, s]
        Maximum overheads associated with the sleep loop.  Depends on CPU speed
        and load, YMMV.

    sleep_fraction [float]
        Once the function has finished its periodic call sleep for a 
        fraction of the remaining time to avoid saturating the processor.

Return value

    overshoot [float, s]
        Overshoot time 

    """
    t_target = time.time() + dt - call_overhead
    while (remaining := t_target - time.time()) >= 0:
        if remaining > sleep_overhead:
            time.sleep(remaining * sleep_fraction)
    return -remaining

def sleep_until(
        t: float,
        sleep_overhead: NonNegativeFloat = 1e-3,
        sleep_fraction: StrictFraction = 0.6,
):
    """
Semi-precise sleep function with about microsond accuracy.

Arguments

    t [float, s]: 
        Seconds ellapsed since epoch start, as given by time.time() 

Optional keyword arguments:

    sleep_overhead [float, s]
        Maximum overheads associated with the sleep loop.  Depends on CPU speed
        and load, YMMV.

    sleep_fraction [float]
        Once the function has finished its periodic call sleep for a 
        fraction of the remaining time to avoid saturating the processor.

Return value

    overshoot [float, s]
        Overshoot time 

    """
    while (remaining := t - time.time()) >= 0:
        if remaining > sleep_overhead:
            time.sleep(remaining * sleep_fraction)
    return -remaining 

def periodic_call(
        fun: Callable = None,
        *,
        interval: PositiveFloat = 1,
        initial_delay: NonNegativeFloat = 0.01,
        loop_condition: Callable[[object, int], bool] = lambda r, n: True,
        sleep_fraction: StrictFraction = 0.5, 
        sleep_overhead: NonNegativeFloat = 1e-3,
        call_overhead: NonNegativeFloat = 5e-6,
        threaded: bool = False,
):
    """
Periodically calls a function using semi-precise timing without saturating
processor.  

Optional keyword arguments:

    interval [float, s]
        Interval to call periodically the fonction. 

    initial_delay [float, s]
        Initial delay before the first function call

    loop_condition [function]: 
        A function that takes the result of the function (can be None) and 
        the number of calls made and returns a boolean value. By default, 
        loop forever.  

    sleep_fraction [float]
        Once the function has finished its periodic call sleep for a 
        fraction of the remaining time to avoid saturating the processor.

    sleep_overhead [float, s]
        Maximum overheads associated with the sleep loop.  Depends on CPU speed
        and load, YMMV.

    call_overhead [float, s]
        Typical overhead for a function call and return 

Example use:

    from obstechutils.precise_timing import periodic_call

    @periodic_call(
        interval=30, initial_delay=1,
        loop_condition: lambda res, n: n <= 10
    )
    def f():
        ... 

    if __name__ == "__main__":
        # operation to be repeated every 30s exactly 10 times at times 
        #    t = time.time() + 1 + 30 * n
        # with an offset and variance of microseconds or less depending 
        # on machine and CPU load.  Some outliers with milliseconds may
        # occur, though.
        f()                          

"""
    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            fname = f.__name__
            logger = logging.getLogger('obstechutils')
            logger.info(f'{fname} periodic call every {interval:.4f} s')
          
            n = 0
            t0 = time.time() + initial_delay - call_overhead
            t_target = t0

            while True:

                delay = sleep_until(
                    t_target, 
                    sleep_overhead=sleep_overhead,
                    sleep_fraction=sleep_fraction
                )

                res = f(*args,**kwargs)
                n += 1
                logger.debug(f'{fname} call #{n} dt={delay*1e6:.3f} μs')

                if not loop_condition(res, n):
                    break

                t_target = t0 + n * interval

        if not threaded:
            return wrapper
           
        @wraps(wrapper) 
        def threaded_wrapper(*args, **kwargs):
            t = threading.Thread(
                    target=wrapper, args=args, kwargs=kwargs,
                    daemon=True
            )
            t.start()

        return threaded_wrapper

    if fun:
        return decorator(fun)
    
    return decorator

# We want to avoid any of the time keeping routines to perform a long
# download when speed is required... autoupdate the leap seconds / Earth
# rotation table every day in the background.

@periodic_call(interval=86_400, threaded=True)
def daily_earth_rotation_update():

    from astropy.utils.iers import conf
    
    logger = logging.getLogger('obstechutils')

    max_age = conf.auto_max_age
    download = conf.auto_download
    timeout = conf.remote_timeout
            
    conf.auto_max_age = 10.
    conf.auto_download = True
    conf.remote_timeout = 30
    logging.info('Daily check for Earth rotation update needs')

    for i in range(3):

        try:
            
            t1 = Time.now().tai # leap seconds needed
            t2 = t1.ut1         # Earth rotation needed

        except Exception as e:
            message = "{e}"

        else:

            logger.info('Check done')
            break

    else:

        logger.error('could not update IERS tables, will try again tomorrow.')
        logger.error(f'message was: {message}')

    conf.remote_timeout = timeout
    conf.auto_max_age = max_age
    conf.auto_download = download
  
daily_earth_rotation_update()
