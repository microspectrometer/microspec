# -*- coding: utf-8 -*-
"""Send commands to the dev-kit.

Example
-------

>>> import microspec
>>> kit = microspec.Devkit()

If ``status=='ERROR'`` it means the command or its arguments are
invalid.

TODO(sustainablelab): after receiving an ERROR, flush
serial communication. The flush involves a short timeout (I can't
think of a better way without implementing packets). This is
a serial-flush-timeout is intentional. It is NOT the general
timeout case I cover next.

If ``status=='TIMEOUT'`` it means the command timed out before a
response was received.

For applications that run a long time, such as data loggers and
free-running plot GUIs, there are occasional timeouts when
calling :func:`~micropsec.commands.Devkit.captureFrame`. These
applications should check the
:class:`~micropsec.replies.captureFrame_response.status`
attribute of responses to
:func:`~micropsec.commands.Devkit.captureFrame` and ignore the
data if the status is 'TIMEOUT'.

A ``UserWarning`` is also issued when a timeout occurs,
identifying which command timed out. This is not an exception, so
it does not cause the application to terminate.

Notes
-----
The :class:`~microspec.commands.Devkit` attribute ``timeout``
defaults to 2 seconds, which is usually long enough to send a
command, execute it on the dev-kit, and receive a response back
on the host computer running the application. It is rare to
observe a timeout when sending commands at the REPL or executing
a script that runs a few commands and exits. Users can observe
a timeout condition by setting a very short timeout such as 1ms.

"""

__all__ = ['Devkit']

from microspeclib.simple import MicroSpecSimpleInterface
from microspec.constants import *
from microspec.helpers import *
import microspec.replies as replies
import warnings

def raise_TypeError_if_any_int_args_are_negative(args: dict={}) -> None:
    """Raise TypeError if any int arguments are negative.

    Notes
    -----

    :mod:`microspeclib` uses ``struct.pack()` to translate the
    command and its arguments into a byte sequence to send over
    serial.

    See: https://docs.python.org/3/library/struct.html#struct.pack

    ``struct.pack()`` takes a "format" argument.

    See: https://docs.python.org/3/library/struct.html#format-characters

    :mod:`microspeclib` uses formats "B", "H", and "L".
    These are unsigned integers, sized 1, 2, and 4 bytes
    respectively.

    Negative parameter values, therefore, are not allowed. But
    :mod:`microspeclib` does not check for negative values. If a
    user passes negative parameter values, the ``struct``
    package's built-in exceptions show-up in the traceback.

    At the level of application development with ``microspec``,
    it is not immediately obvious that the problem is due to
    using a negative value.
    
    ``microspec`` deals with this by checking for negative
    parameter values in :class:`Devkit`.

    Note: the dev-kit firmware already rejects out-of-range
    values with an ERROR status, but it cannot reject a value if
    the application exits due to an exception, and it needs to be
    clear to the user what the cause of the exception is.

    Example
    -------

    >>> import microspec as usp
    >>> kit = usp.Devkit() #doctest: +SKIP
    >>> kit.getBridgeLED(led_num = -1) #doctest: +SKIP
    Traceback (most recent call last):
    ...
    TypeError: Parameter 'led_num' must be non-negative.
    """
    # Loop through the arguments.
    for key in args:
        # Only consider int arguments.
        if type(args[key]) == int:
            # Raise an error if it is negative.
            if args[key] < 0:
                raise TypeError(
                    f"Parameter '{key}' must be non-negative."
                    )

class TimeoutHandler():
    """Handle case where serial communication timed out.
    
    :mod:`microspeclib` provides a user-configurable timeout. The
    timeout sets how long to wait after sending a command. The return
    value is ``None`` if a response is not received in that time.

    Checking for a ``None`` return value is the only way to determined
    that the command timedout.

    Note this is different from an ``ERROR``. An ``ERROR`` **is** a
    response from the firmware. It means the firmware did not understand
    the command and the subsequent data received should be ignored.

    This class, therefore, adds that missing functionality:

    - if a TIMEOUT occurred (if the command return value is ``None``):

        - :func:`warn_if_cmd_timedout` issues the ``UserWarning``
        - :func:`is_out_of_time` returns ``True``

            - the caller code (the command) is able to return an
              appropriate response instead of ``None``

    """

    def _issue_timeout_warning(self,
            command_name : str,
            suggestion : str = ""
            ):
        warnings.warn(
            f"Command {command_name} timed out. {suggestion}",
            stacklevel=4
            )
    def is_out_of_time(self, reply):
        """Return True if the command timed out.

        This is a small helper to make caller code (the command)
        readable.

        It also enables testing the condition that the command
        timed out:

        - creates a seam where the unit tests monkeypatch a
          timeout condition by making this function always return
          ``True``
        - returning ``True`` tests two code branches:

            - func:`warn_if_cmd_timedout` issues a timeout
              ``UserWarning``
            - caller (the command) creates a TIMEOUT reply
              instead of the usual reply

        Parameters
        ----------
        reply:
            The return value of the
            :class:`~microspeclib.simple.MicrospecSimpleInterface`
            command, *not* the return value of the commands
            defined in :class:`Devkit`.
        """
        return True if reply == None else False
    def warn_if_cmd_timedout(self,
            reply,
            command_name: str,
            suggestion: str = ""
            ) -> None:
        """Issue a warning if the command timed out.

        Parameters
        ----------
        reply:
            The return value of the
            :class:`~microspeclib.simple.MicrospecSimpleInterface`
            command, *not* the return value of the commands
            defined in :class:`Devkit`.
        command_name: str
            The :class:`Devkit` method name, e.g., "captureFrame".
        suggestion: str
            A message to the user on how to troubleshoot the
            timeout. If omitted or an empty string, a standard
            suggestion is used.
        """
        # Define a default suggestion if no suggestion is given.
        # default = (""
        #         "Expect this is a rare hardware event. "
        #         f"Retry {command_name} and increase the timeout "
        #         "if the command timed out again. "
        #         "If that does not help, "
        #         "try a different USB cable or USB port, "
        #         "or a different host computer."
        #         )
        # suggestion = default if suggestion == "" else suggestion
        if self.is_out_of_time(reply):
            self._issue_timeout_warning(command_name, suggestion)

class Devkit(MicroSpecSimpleInterface, TimeoutHandler):
    """Interface for dev-kit communication.

    Every communication with the dev-kit consists of:

    - a **command** sent to the dev-kit
    - a **response** received from the dev-kit

    Calling a ``Devkit`` method sends the **command**. The method's
    return value is the **response**.

    Example
    -------

    Command ``getBridgeLED`` returns ``getBridgeLED_response``:

    >>> import microspec
    >>> kit = microspec.Devkit()
    >>> kit.getBridgeLED()
    getBridgeLED_response(status='OK', led_setting='GREEN')

    Assign the **response** to variable ``reply``:

    >>> reply = kit.getBridgeLED()

    Access each part of the response as attributes ``status`` and
    ``led_setting``:

    >>> reply.status
    'OK'
    >>> reply.led_setting
    'GREEN'

    """

    def __init__(self):
        """Add attributes to Devkit. Sync status. Comm check.
        
        - Add some convenience attributes (see Attributes below).
        - Get exposure time.
        - Get autoexpose configuration.
        
        Check communications: if the first attempt at
        communication (get exposure time) timeouts, something is
        wrong. Close communication and tell the user how to
        troubleshoot. Client code tests for this condition by
        checking `if timedout is True`::

            import microspec as usp
            kit = usp.Devkit()
            if kit.timedout is True:
                # Tell user something useful
                print(kit.trouble_msg)

        Attributes
        ----------
        exposure_time_cycles: int
            Exposure time in cycles. Updated every time getExposure()
            and setExposure() are called.
        exposure_time_ms: ms
            Exposure time in ms. Updated every time getExposure()
            and setExposure() are called.
        timedout: bool
            True if the most recent command timedout.
        trouble_msg: string
            This is the troubleshooting message printed to
            stdout. This message is also stored as attribute
            ``trouble_msg`` as a convenience for the client
            application to use this message (e.g., status text in
            a GUI).
        """
        super().__init__()
        self.timedout = False
        self.trouble_msg = ""
        # Initialize exposure_time_ attrs (sync with dev-kit)
        reply = self.getExposure()

        # If this first attempt at communication timeouts,
        # there's probably something wrong with the serial
        # connection.
        #
        # Either the usb-bridge is not connected to the
        # vis-spi-out board,
        # OR they are connected but the slider switch is set to
        # ISP (firmware programming) instead of SPI (serial communication).

        try:
            assert reply.status != 'TIMEOUT'

            # We did not TIMEOUT, so communication is good. Yay.
            # Go ahead and finish initilization: sync dev-kit
            # info with this instance of Devkit.

            # Initialize autoexpose_ attrs (sync with dev-kit)
            self.getAutoExposeConfig()

            # Get the sensor hash to figure out LIS or S13131.
            # I'm using AttributeError as a quick kludge for
            # backwards compatibility.
            try:
                reply = self.getSensorHash()
                # TODO(slab): put all of this in the getSensorHash wrapper
                # """
                # >>> import microspec as usp;
                # >>> kit = usp.Devkit()
                # >>> kit.sensor_name
                # 'LIS-770i'
                # """
                b1 = reply.first_byte
                b2 = reply.second_byte
                b3 = reply.third_byte
                self.sensor_hash = (b1<<16) | (b2<<8) | b3
                if self.sensor_hash == 0x351ea9:
                    self.sensor_name = "LIS-770i"
                elif self.sensor_hash == 0x91d318:
                    self.sensor_name = "S13131-512"
                else:
                    self.sensor_name = "Unknown"
                    self.sensor_hash = 0x123456
            except AttributeError:
                # 'tis the old firmware. Therefore, it's a LIS.
                self.sensor_name = "LIS-770i"
                self.sensor_hash = 0x351ea9
        except AssertionError:
            # Initial attempt at communication TIMEDOUT.
            # Set timedout True so caller code can check for this case.
            # Output a useful troubleshooting message.
            self.serial.close()
            self.timedout = True
            self.trouble_msg = (
                "ERROR: usb-bridge cannot communicate with vis-spi-out.\n"
                "STATUS: Serial communication is closed.\n"
                "TROUBLESHOOT:\n"
                "Please check:\n"
                "  1. usb-bridge board is CONNECTED to a vis-spi-out board\n"
                "  2. The BLACK slide switch on the usb-bridge is SET TO `SPI`\n"
                "    - slide the black switch TOWARDS the big shrouded header\n"
                "    - the position of the white switch does not matter\n"
                "After you fix the hardware:\n"
                "  - cycle power to the dev-kit\n"
                "  - try instantiating Devkit() again"
                )
            print(self.trouble_msg)


    def warn_sensor_is_not_LIS(self, command_name : str):
        """Warn user they sent getSensorConfig to a dev-kit that does not use the LIS-770i.
        """
        warnings.warn(
            f"Command {command_name} returned ERROR because "
            "this dev-kit does not use the LIS-770i.",
            stacklevel=2
            )

    def warn_sensor_is_not_LIS_or_config_is_invalid(self, command_name : str):
        """Warn user they failed to set the config.

        The user either sent invalid config values, or the
        dev-kit does not use the LIS-770i.
        """
        warnings.warn(
            f"Command {command_name} returned ERROR because it "
            "failed to set the config, i.e., this command had no "
            "effect on the spectrometer. "
            "Either the config values are invalid or "
            "this dev-kit does not use the LIS-770i.",
            stacklevel=2
            )

    def flush_read_buffer(self):
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        self.null()
        # print("sent 10 nulls - ya happy now?")
        _timeout = self.timeout
        self.timeout = 0.1
        # TODO(sustainablelab): Use serialutil Timeout to replace
        # read_until with my own read_until_timeout
        self.serial.read_until()
        self.timeout = _timeout

    def getBridgeLED(
            self,
            led_num: int = 0 # LED0 is the only Bridge LED
            ):
        """Read the state of the indicator LED on the Bridge PCB.

        Examples
        --------

        *Setup* -- set the LED to a known state:

        >>> import microspec as usp
        >>> kit = usp.Devkit()
        >>> kit.setBridgeLED(led_num=0, led_setting=usp.GREEN)
        setBridgeLED_response(status='OK')

        Call ``getBridgeLED``:

        >>> kit.getBridgeLED()
        getBridgeLED_response(status='OK', led_setting='GREEN')

        See Also
        --------
        setBridgeLED

        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        _reply = super().getBridgeLED(led_num)
        reply = replies.getBridgeLED_response(
            status = status_dict.get(_reply.status),
            led_setting = led_dict.get(_reply.led_setting)
            )
        # TODO(sustainablelab): add this to *every* command?
        # Except what I *really* want to do is only follow this
        # branch when the usb-bridge replies ERROR. If the
        # usb-bridge is OK and the vis-spi-out replies ERROR,
        # that's fine because the usb-bridge sends PADDING bytes
        # back to the host. In other words, serial communication
        # is still in sync.
        #
        # if reply.status == 'ERROR':
        #     self.flush_read_buffer()
        return reply

    def setBridgeLED(
            self,
            led_setting: int,
            led_num: int = 0 # LED0 is the only Bridge LED
            ):
        """Set the LED on the Bridge PCB to OFF, GREEN, or RED.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        Call ``setBridgeLED`` with optional parameter ``led_num``:

        >>> kit.setBridgeLED(led_num=0, led_setting=usp.GREEN)
        setBridgeLED_response(status='OK')

        Call ``setBridgeLED`` without optional parameter ``led_num``:

        >>> kit.setBridgeLED(led_setting=usp.GREEN)
        setBridgeLED_response(status='OK')

        Call ``setBridgeLED`` with an invalid parameter value:

        >>> kit.setBridgeLED(led_num=1, led_setting=usp.GREEN)
        setBridgeLED_response(status='ERROR')

        See Also
        --------
        getBridgeLED
        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        _reply = super().setBridgeLED(led_num, led_setting)
        reply = replies.setBridgeLED_response(
            status = status_dict.get(_reply.status)
            )
        return reply

    def getSensorLED(
            self,
            led_num : int
            ):
        """Read the state of an indicator LED on the Sensor PCB.

        There are two indicator LEDS: led0 and led1.

        .. note::

            Application code should never call this method:

            - led0 is OFF while commands execute, so the state returned
              by :func:`microspec.commands.Devkit.getSensorLED` is
              always OFF
            - led1 indicates the success of auto-expose, but this is
              directly available from the ``success`` attribute of the
              response to :func:`microspec.commands.Devkit.autoExposure`

        Examples
        --------

        *Setup* -- set the LEDs to a known state:

        >>> import microspec as usp
        >>> kit = usp.Devkit()
        >>> kit.setSensorLED(usp.GREEN, led_num=0)
        setSensorLED_response(status='OK')
        >>> kit.setSensorLED(usp.GREEN, led_num=1)
        setSensorLED_response(status='OK')

        Call ``getSensorLED``:

        >>> kit.getSensorLED(0) # Expect OFF
        getSensorLED_response(status='OK', led_setting='OFF')
        >>> kit.getSensorLED(1) # Expect GREEN
        getSensorLED_response(status='OK', led_setting='GREEN')

        See Also
        --------
        setSensorLED
        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        # Send command and get low-level reply.
        _reply = super().getSensorLED(led_num)

        # Create high-level reply.
        reply = replies.getSensorLED_response(
                status = status_dict.get(_reply.status),
                led_setting = led_dict.get(_reply.led_setting)
                )

        return reply

    def setSensorLED(
            self,
            led_setting : int,
            led_num : int
            ):
        """Set the LEDs on the Sensor PCB to OFF, GREEN, or RED.

        There are two indicator LEDS:

        - led0

            - usually appears GREEN
            - is OFF while a command is being executed
            - only turns RED if there is a serious error in serial
              communication (this should never happen)

        - led1

            - usually appears GREEN
            - turns RED during auto-expose
            - stays RED if auto-expose fails
            - turns GREEN if auto-expose succeeds

        .. note::

            Application code should never call this method. The LEDs are
            controlled by firmware to indicate status. Controlling the
            LEDs from the application undermines the LEDs purpose as
            status indicators.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit() #doctest: +SKIP

        Turn led0 and led1 OFF:

        >>> kit.setSensorLED(usp.OFF, 0) #doctest: +SKIP
        setSensorLED_response(status='OK')
        >>> kit.setSensorLED(usp.OFF, 1) #doctest: +SKIP
        setSensorLED_response(status='OK')

        Turn led0 and led1 RED:

        >>> kit.setSensorLED(usp.RED, 0) #doctest: +SKIP
        setSensorLED_response(status='OK')
        >>> kit.setSensorLED(usp.RED, 1) #doctest: +SKIP
        setSensorLED_response(status='OK')

        Turn led0 and led1 GREEN:

        >>> kit.setSensorLED(usp.GREEN, 0) #doctest: +SKIP
        setSensorLED_response(status='OK')
        >>> kit.setSensorLED(usp.GREEN, 1) #doctest: +SKIP
        setSensorLED_response(status='OK')

        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        _reply = super().setSensorLED(led_num, led_setting)
        reply = replies.setSensorLED_response(
                status = status_dict.get(_reply.status)
                )
        return reply

    def getSensorConfig(self):
        """One-liner

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()
        >>> kit.setSensorConfig() # restore default config
        setSensorConfig_response(status='OK')

        Read the spectrometer's pixel configuration:

        >>> kit.getSensorConfig()
        getSensorConfig_response(status='OK', binning='BINNING_ON',
                                 gain='GAIN1X', row_bitmap='ALL_ROWS',
                                 row_bitmap_int=31)
        """

        # Send command and get low-level reply.
        _reply = super().getSensorConfig()

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="getSensorConfig")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create high-level reply. Use bad data if there was a timeout.
        if TIMEOUT:
            reply = replies.getSensorConfig_response(
                    status     = 'TIMEOUT',
                    binning    = '', # <--- bad data
                    gain       = '', # <--- bad data
                    row_bitmap = ''  # <--- bad data
                    )
        else:
            # Return the rows as a string by converting the 5-bit
            # bitmask to a str such as "ROW1 | ROW2 | ROW3"
            # and if all rows are on, just return str "ALL_ROWS"
            if _reply.row_bitmap == ALL_ROWS:
                rows_str = row_dict.get(_reply.row_bitmap)
            else:
                # Build str array of the rows that are on
                rows = [ROW1, ROW2, ROW3, ROW4, ROW5] # int array
                rows_on = [] # str array
                for row in rows:
                    if _reply.row_bitmap & row:
                        rows_on.append(row_dict.get(row))
                # Convert array to a single string
                rows_str = "|".join(rows_on)
            reply = replies.getSensorConfig_response(
                    status     = status_dict.get(_reply.status),
                    binning    = binning_dict.get(_reply.binning),
                    gain       = gain_dict.get(_reply.gain),
                    row_bitmap = rows_str,
                    row_bitmap_int = _reply.row_bitmap
                    # Return as str AND int as a convenience.
                    # Returning a str OR an int is confusing.
                    # row_bitmap = (
                    #     row_dict.get(_reply.row_bitmap)
                    #     if _reply.row_bitmap == ALL_ROWS
                    #     else _reply.row_bitmap
                    #     )
                    )

        # Handle case where vis-spi-out does not recognize this
        # command because it is not programmed for the LIS.

        if reply.status == 'ERROR':
            self.warn_sensor_is_not_LIS("getSensorConfig")

        return reply

    def setSensorConfig(
            self,
            binning : int = BINNING_ON,
            gain : int = GAIN1X,
            row_bitmap : int = ALL_ROWS
            ):
        """One-liner

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit() #doctest: +SKIP

        Configure the spectrometer with pixel binning off:

        >>> kit.setSensorConfig(binning=usp.BINNING_OFF) #doctest: +SKIP
        setSensorConfig_response(status='OK')
        >>> kit.getSensorConfig() #doctest: +SKIP
        getSensorConfig_response(status='OK', binning='BINNING_OFF',
                                 gain='GAIN1X', row_bitmap='ALL_ROWS')

        Configure the spectrometer with the default pixel configuration:

        >>> kit.setSensorConfig() #doctest: +SKIP
        setSensorConfig_response(status='OK')
        >>> kit.getSensorConfig() #doctest: +SKIP
        getSensorConfig_response(status='OK', binning='BINNING_ON',
                                 gain='GAIN1X', row_bitmap='ALL_ROWS')

        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        _reply = super().setSensorConfig(binning, gain, row_bitmap)
        reply = replies.setSensorConfig_response(
                status_dict.get(_reply.status)
                )
        if reply.status == 'ERROR':
            self.warn_sensor_is_not_LIS_or_config_is_invalid("setSensorConfig")
        return reply

    def setExposure(
            self,
            ms : float = None,  # specify time in milliseconds
            cycles : int = None # OR time in cycles
            ):
        """Tell the dev-kit how long to expose the detector.

        This updates exposure time attrs ``exposure_time_cycles``
        and ``exposure_time_ms`` using the input argument. If you
        want to be certain the exposure time attrs are synced
        with the dev-kit, follow this with a ``getExposure()``
        call.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        ``setExposure`` accepts time in units of ms:

        >>> kit.setExposure(ms=5.0)
        setExposure_response(status='OK')

        ``setExposure`` accepts time in units of cycles:

        >>> kit.setExposure(cycles=250)
        setExposure_response(status='OK')

        ``setExposure`` requires an exposure time input

        >>> kit.setExposure()
        Traceback (most recent call last):
            ...
        TypeError: setExposure() missing 1 required argument: 'ms' or 'cycles'

        Calling ``setExposure`` with both ``ms`` and ``cycles`` is not
        allowed:

        >>> kit.setExposure(ms=5.0, cycles=250)
        Traceback (most recent call last):
            ...
        TypeError: setExposure() got an unexpected keyword 'cycles'
        (requires 'ms' or 'cycles' but received both)

        Exposure time must be within the allowed range:

        >>> # Min exposure time in milliseconds:
        >>> usp.to_ms(usp.MIN_CYCLES)
        0.02
        >>> # Max exposure time in milliseconds:
        >>> usp.to_ms(usp.MAX_CYCLES)
        1310.0
        >>> # Try exceeding maximum exposure:
        >>> kit.setExposure(cycles=usp.MAX_CYCLES+1)
        Traceback (most recent call last):
        ...
        TypeError: Exposure time cannot be more than 65500 cycles.

        >>> # Try exposure time below the minimum:
        >>> kit.setExposure(cycles=usp.MIN_CYCLES-1)
        Traceback (most recent call last):
        ...
        TypeError: Exposure time cannot be less than 1 cycles.

        """

        raise_TypeError_if_any_int_args_are_negative(locals())

        # Exposure time units are either ms or cycles
        if ms == None and cycles == None:
            raise TypeError(
                "setExposure() missing 1 required argument: "
                "'ms' or 'cycles'"
                )
        if ms != None and cycles != None:
            raise TypeError(
                "setExposure() got an unexpected keyword "
                "'cycles' (requires 'ms' or 'cycles' but "
                "received both)"
                )
        if ms == None: time = cycles
        else: time = to_cycles(ms)

        # Raise an error if exposure time is outside the valid range.
        if time < MIN_CYCLES:
            raise TypeError(
                "Exposure time cannot be less than "
                f"{MIN_CYCLES} cycles."
                )
        if time > MAX_CYCLES:
            raise TypeError(
                "Exposure time cannot be more than "
                f"{MAX_CYCLES} cycles."
                )

        # Send command and get low-level reply.
        _reply = super().setExposure(time)

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="setExposure")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create high-level reply.
        reply = replies.setExposure_response(
                'TIMEOUT'
            ) if TIMEOUT else replies.setExposure_response(
                status_dict.get(_reply.status)
                )

        # Update Devkit exposure time attrs
        if reply.status == 'OK':
            self.exposure_time_cycles = time
            self.exposure_time_ms = to_ms(time)

        return reply

    def getExposure(self):
        """Ask the dev-kit how long it exposes the detector.

        In addition to returning exposure time in the reply, this
        call updates the exposure time attrs
        ``exposure_time_cycles`` and ``exposure_time_ms`` as a
        convenient alternative to parsing the reply and storing
        these values yourself.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        ``getExposure`` reports exposure time in both units:

        >>> # Setup: set exposure time to 5ms
        >>> kit.setExposure(ms=5)
        setExposure_response(status='OK')
        >>> # Test: expect 5.0ms and 250 cycles
        >>> kit.getExposure()
        getExposure_response(status='OK', ms=5.0, cycles=250)
        """

        # Send command and get low-level reply.
        _reply = super().getExposure()

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="getExposure")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create high-level reply. Use bad data if there was a timeout.
        reply = replies.getExposure_response(
                status = 'TIMEOUT',
                ms     = 0, # <--- bad data
                cycles = 0  # <--- bad data
            ) if TIMEOUT else replies.getExposure_response(
                status = status_dict.get(_reply.status),
                ms     = to_ms(_reply.cycles),
                cycles = _reply.cycles
                )

        # Update Devkit exposure time attrs
        if reply.status == 'OK':
            self.exposure_time_cycles = reply.cycles
            self.exposure_time_ms = reply.ms

        return reply

    def captureFrame(self):
        """Expose the detector and readout one frame.

        Return
        ------
        status : str
            Serial communication status, either 'OK', 'ERROR', or
            'TIMEOUT'.
        num_pixels : int
            The number of pixels in the frame (either 392 or 784
            depending on pixel binning).
        pixels : list
            The 16-bit ADC counts at each pixel, starting with pixel 1
            and ending with pixel 392 or 784 (depending on pixel
            binning).
        frame : dict
            Python dictionary where the key is the pixel number and
            the value is the 16-bit ADC counts at that pixel.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        Capture a frame:

        >>> reply = kit.captureFrame()

        The frame is stored as a Python ``list`` of numbers. Each
        number is the signal strength at that pixel in units of
        *counts*.

        The list starts with pixel 1. With pixel binning on, the
        frame has 392 pixels, so the list ends with pixel 392:

        >>> print(reply)
        captureFrame_response(status='OK', num_pixels=392,
                              pixels=[...], frame={...})

        The list ``pixels`` is hard to read on its own (index 0
        is pixel 1, index 1 is pixel 2, etc.):

        >>> print(reply.pixels)
        [..., ..., ...]

        It is usually more convenient for applications to use the
        dict ``frame`` because it tags each pixel with its pixel
        number:

        >>> print(reply.frame)
        {1: ..., 2: ..., ..., 391: ..., 392: ...}

        This is still hard to read in the REPL. Put each pixel on
        its own line:

        >>> import pprint
        >>> pprint.pprint(reply.frame)
        {1: ...,
         2: ...,
         ...
         391: ...,
         392: ...}

        Alternatively, turn the ``(pixel number, pixel value)``
        pairs into a list of ``tuples``:

        >>> frame = list(zip(range(1,reply.num_pixels+1), reply.pixels))
        >>> pprint.pprint(frame)
        [(1, ...),
         (2, ...),
         ...,
         (391, ...),
         (392,...)]

        Notes
        -----
        If there is a timeout, :func:`captureFrame` returns
        ``status='TIMEOUT'``, and fills the reply with obviously
        bad data:

            - ``num_pixels=0``
            - ``pixels=[]``
            - ``frame={}``

        Applications are protected from accidentally setting a
        :attr:`Devkit.timeout` that is shorter than the exposure
        time (because this *guarantees* that :func:`captureFrame`
        timeouts before a response is received).

        If the timeout is less than the exposure time,
        :func:`captureFrame` uses a :attr:`Devkit.timeout` that
        is one second longer than the exposure time.

        If an application loops :func:`captureFrame` for a long
        time (such as the data logging and plotting GUI examples
        above), there will likely be a timeout.

        In this case, :func:`captureFrame` issues a
        ``UserWarning`` describing which command caused the
        timeout.

            This is only a warning because the timeout is
            hardware-dependent. It does **not** indicate a bug in
            the application code.

        The timeout ``UserWarning`` prints to the console and can
        safely be ignored. If the timeouts are a frequent event,
        it indicates a problem with the host computer, its USB
        port, or the USB cable.

        """
        # -----------------------------------
        # | Prevent timeout < exposure_time |
        # -----------------------------------
        # ---BEGIN---

        # Save the user's timeout to restore later.
        _timeout = self.timeout

        # Prevent case that timeout < exposure_time.
        if self.timeout*1000 < self.exposure_time_ms:

            # Set timeout one second longer than exposure time.
            self.timeout = self.exposure_time_ms/1000 + 1

        # Now it is safe to capture a frame.
        _reply = super().captureFrame()

        # Restore the user's timeout.
        self.timeout = _timeout

        # ---END---

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="captureFrame")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create the reply. Use bad data if there was a timeout.
        reply = replies.captureFrame_response(
                    status = 'TIMEOUT',
                    num_pixels = 0, # <--- bad data
                    pixels = [], # <------ bad data
                    frame = {} # <-------- bad data
                ) if TIMEOUT else replies.captureFrame_response(
                    status = status_dict.get(_reply.status),
                    num_pixels = _reply.num_pixels,
                    pixels = _reply.pixels,
                    # Format data into a "frame" dict where:
                    # - pixel number is the key
                    # - pixel ADC counts is the value
                    frame = dict(zip(
                        range(1,_reply.num_pixels+1), # <- pixel number 1:N
                        _reply.pixels) # <---------------- counts
                        )
                    )

        return reply

    def autoExposure(self):
        """Auto-expose the spectrometer.

        Tell dev-kit firmware to adjust spectrometer exposure time until
        peak signal strength hits the auto-expose target.

        Returns
        -------
        :class:`~microspec.replies.autoExposure_response`
          - status
          - success
          - iterations


        See Also
        --------
        setAutoExposeConfig: configure auto-expose parameters
        getExposure: get the new exposure time after the auto-expose


        Examples
        --------

        >>> kit.autoExposure() # doctest: +SKIP
        autoExposure_response(status='OK', success='GAVE_UP', iterations=4)

        """

        # Send command and get low-level reply.
        _reply = super().autoExposure()

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="autoExposure")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create high-level reply. Use bad data if there was a timeout.
        reply = replies.autoExposure_response(
                status = 'TIMEOUT',
                success = '', # <------- bad data
                iterations = 0, # <----- bad data
            ) if TIMEOUT else replies.autoExposure_response(
                status = status_dict.get(_reply.status),
                success = success_dict.get(_reply.success),
                iterations = _reply.iterations
                )

        return reply

    def getAutoExposeConfig(self):
        """Ask the dev-kit how it's auto-expose is configured.

        In addition to returning the autoexpose config in the
        reply, this call updates the autoexpose attrs as a
        convenient alternative to parsing the reply and storing
        these values yourself.

        These are the autoexpose attrs:

            - ``autoexpose_max_tries``
            - ``autoexpose_start_pixel``
            - ``autoexpose_stop_pixel``
            - ``autoexpose_target``
            - ``autoexpose_target_tolerance``
            - ``autoexpose_max_exposure``

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        See what the auto-expose parameters are:
        >>> kit.getAutoExposeConfig()
        getAutoExposeConfig_response(status='OK', max_tries=12,
                                    start_pixel=7, stop_pixel=392,
                                    target=46420, target_tolerance=3277,
                                    max_exposure=10000)

        """

        # Send command and get low-level reply.
        _reply = super().getAutoExposeConfig()

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="getAutoExposeConfig")
        TIMEOUT = self.is_out_of_time(_reply)

        # Create high-level reply. Use bad data if there was a timeout.
        reply = replies.getAutoExposeConfig_response(
                status = 'TIMEOUT',
                max_tries        = 0, # <--- bad data
                start_pixel      = 0, # <--- bad data
                stop_pixel       = 0, # <--- bad data
                target           = 0, # <--- bad data
                target_tolerance = 0, # <--- bad data
                max_exposure     = 0  # <--- bad data
            ) if TIMEOUT else replies.getAutoExposeConfig_response(
                status           = status_dict.get(_reply.status),
                max_tries        = _reply.max_tries,
                start_pixel      = _reply.start_pixel,
                stop_pixel       = _reply.stop_pixel,
                target           = _reply.target,
                target_tolerance = _reply.target_tolerance,
                max_exposure     = _reply.max_exposure
                )

        # Update Devkit autoexpose attrs
        if reply.status == 'OK':
            self.autoexpose_max_tries = reply.max_tries
            self.autoexpose_start_pixel = reply.start_pixel
            self.autoexpose_stop_pixel = reply.stop_pixel
            self.autoexpose_target = reply.target
            self.autoexpose_target_tolerance = reply.target_tolerance
            self.autoexpose_max_exposure = reply.max_exposure
        return reply

    def setAutoExposeConfig(
            self,
            max_tries : int = 12,
            start_pixel : int = 7,
            stop_pixel : int = 392,
            target : int = 46420,
            target_tolerance : int = 3277,
            max_exposure : int = 10000
            ):
        """Write a new autoexpose configuration to the dev-kit.

        This updates autoexpose attrs using the input arguments.

        These are the autoexpose attrs:

            - ``autoexpose_max_tries``
            - ``autoexpose_start_pixel``
            - ``autoexpose_stop_pixel``
            - ``autoexpose_target``
            - ``autoexpose_target_tolerance``
            - ``autoexpose_max_exposure``

        If you want to be certain the autoexpose attrs are synced
        with the dev-kit, follow this with a
        ``getAutoExposeConfig()`` call.

        Examples
        --------

        *Setup*:

        >>> import microspec as usp
        >>> kit = usp.Devkit()

        Configure auto-expose with the default parameters...:

        >>> kit.setAutoExposeConfig()
        setAutoExposeConfig_response(status='OK')

        See what the new auto-expose parameters are:

        >>> kit.getAutoExposeConfig()
        getAutoExposeConfig_response(status='OK', max_tries=12,
                                    start_pixel=7, stop_pixel=392,
                                    target=46420, target_tolerance=3277,
                                    max_exposure=10000)

        """
        raise_TypeError_if_any_int_args_are_negative(locals())

        # Send command and get low-level reply.
        _reply = super().setAutoExposeConfig(
                            max_tries,
                            start_pixel,
                            stop_pixel,
                            target,
                            target_tolerance,
                            max_exposure
                            )

        # Handle case where the command timed out.
        self.warn_if_cmd_timedout(_reply, command_name="setAutoExposeConfig")
        TIMEOUT = self.is_out_of_time(_reply)

        # TODO: delete this after firmware bug is fixed.
        #
        # FIRMWARE BUG:
        # ``max_exposure`` is sometimes written with 4112 instead of
        # whatever value (specified or default) is passed with the
        # command.
        #
        # This is a firmware bug. Don't know why it happens.
        #
        # The bug is repeatable:
        # Call setAutoExposeConfig followed by getAutoExposeConfig about
        # four or five times. Initially they all work as expected, then
        # they start alternating:
        # every other time setAutoExposeConfig is called, the
        # max_exposure gets set to 4112:
        # >>> kit.setAutoExposeConfig(); reply1 = kit.getAutoExposeConfig();
        # ... kit.setAutoExposeConfig(); reply2 = kit.getAutoExposeConfig();
        # ... print(f"{reply1.max_exposure}, {reply2.max_exposure}")
        # 10000, 4112
        #
        # TEMPORARY FIX:
        # Check if max_exposure if 4112. If so, just setAutoExposeConfig
        # again. I have not observed 4112 written consecutively.
        # Test that this fix is good enough:
        # >>> for i in range(1,1000):
        # ...    kit.setAutoExposeConfig()
        # ...    reply = kit.getAutoExposeConfig()
        # ...    if i%100 == 0: print(i)
        # ...    if reply.max_exposure != 10000: print(reply.max_exposure)
        # 100
        # 200
        # 300
        # 400
        # 500
        # 600
        # 700
        # 800
        # 900
        if self.getAutoExposeConfig().max_exposure == 4112:
            # max exposure is 4096+16 (0x1010) (0b 0001 0000 0001 0000)
            # Re-Send command and get low-level reply.
            # print("Gotta fix this bug man!")
            _reply = super().setAutoExposeConfig(
                                max_tries,
                                start_pixel,
                                stop_pixel,
                                target,
                                target_tolerance,
                                max_exposure
                                )

        # Create high-level reply.
        reply = replies.setAutoExposeConfig_response(
                    'TIMEOUT'
                ) if TIMEOUT else replies.setAutoExposeConfig_response(
                    status_dict.get(_reply.status)
                )

        # Update Devkit autoexpose attrs
        if reply.status == 'OK':
            self.autoexpose_max_tries = max_tries
            self.autoexpose_start_pixel = start_pixel
            self.autoexpose_stop_pixel = stop_pixel
            self.autoexpose_target = target
            self.autoexpose_target_tolerance = target_tolerance
            self.autoexpose_max_exposure = max_exposure

        return reply
