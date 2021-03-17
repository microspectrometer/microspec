__all__ = [
    'to_cycles',
    'to_ms'
    ]
def to_cycles(ms : float) -> int:
    u"""Convert exposure time from milliseconds to cycles.

    Parameters
    ----------
    ms
        Exposure time in milliseconds.

    Returns
    -------
    int
        Exposure time in cycles.

    Example
    -------

    >>> import microspec as usp
    >>> usp.to_cycles(ms=0.8)
    40

    Notes
    -----
    The conversion is simply time [ms] * 50 [cycles/ms]

    The general dimensional analysis is::

        (ms * s/ms)/(s/cycle)

    Simplifying::

        (ms / 1000) * (cycles/s)

    Substituting s/cycle = 20e-6, then cycles/s = 50e3

    Simplifying again::

        (ms / 1000) * (50 000)
        (ms / 1) * (50)

    Lastly, I round the result to guard against the user passing
    a milliseconds value with precision exceeding 1 cycle
    (0.02ms).

    See Also
    --------
    to_ms
    """

    return round(ms*50)

def to_ms(cycles: int) -> float:
    u"""Convert from cycles to milliseconds.

    Parameters
    ----------
    cycles
        Time in cycles. One cycle is 20µs.

    Returns
    -------
    float
        Time in milliseconds.

    Example
    -------

    >>> import microspec as usp
    >>> usp.to_ms(cycles=usp.MAX_CYCLES)
    1310.0

    Notes
    -----
    Dev-kit firmware measures exposure time in units of cycles
    and stores exposure time as a 16-bit unsigned integer. One
    cycle is 20µs because the firmware clocks the detector at
    50kHz. Multiply cycles by 20e-6 to get seconds and by 20e-3
    to get milliseconds.

    The smallest exposure time is 2 cycles (40µs). The largest
    exposure time is 65500 (1.31s).

    Multiplying by 20e-3 is not hard, so why does this helper
    exist? Because multiplying by 0.02 is not quite correct
    because of floating point representation:

    I expect 35 cycles * 0.02 ms/cycle is 0.7ms:
    >>> 35*20e-3
    0.7000000000000001 

    Close, but not 0.7ms!
    One way to get the correct answer:
    >>> round(35*20e-3, ndigits=2)
    0.7

    Even better, how about we think about why 0.7000...01 happens:
    >>> 35*20/1000
    0.7

    See Tom Forsyth's TiddlyWiki: https://tomforsyth1000.github.io/blog.wiki.html
    and search for "A matter of precision". Here is Tom's
    example:

    The answer to this *should be* 11e-7:
    count:1234567
    >>> 1.0000011 - 1.0
    1.09999999997612e-06

    That answer is wrong (though very close).

    These answers are *close enough*, so why do I care? In my
    case, my GUI expects a result with a few digits. I could get
    that from rounding. Or, I can change floating-point
    calculations to fixed-point calculations.

    Using Tom's example again:

    >>> (10000011 - 10000000)/10000000
    1.1e-06

    Lastly, note that ``to_cycles`` *does* round because cycles
    cannot be a fraction (cycles must be a natural number in the
    range [2,65500]). Rounding takes an arbitrary time and picks
    the number of cycles that is the closest to that time.

    See Also
    --------
    to_cycles
    """

    return cycles*20/1000 # NOTE(slab): 20/1000 is right, 20e-3 is wrong

