from .temperature_logger_abstract import TemperatureLoggerAbstract
from .tc08usb import TC08USB, USBTC08_TC_TYPE


class TemperatureLogger(TemperatureLoggerAbstract):
    """
    USB temperature logger TC08 (with 8 thermocouples) 
    """

    def __init__(self):
        """
        constructor
        """
        self._usb_conn = TC08USB()

    def connect(self):
        """
        Connect to pico thermo logger device

        Returns:
            bool: connection status - True if connected, else False
        """
        is_connected = self._usb_conn.open_unit()
        return bool(is_connected)

    def set_channel(self, channel_number):
        """
        Set thermo couple channel

        Args:
            channel_number (int): thermo couple channel
        """
        self._usb_conn.set_mains(50)
        self._usb_conn.set_channel(channel_number, USBTC08_TC_TYPE.K)

    def read_temperature(self, channel):
        """
        Read thermocouple logger output

        Args:
            channel (int): thermo couple channel

        Returns:
            float: temperature value read
        """
        self._usb_conn.get_single()
        return self._usb_conn[channel]

    def close_connection(self):
        """
        Close connection to device
        """
        self._usb_conn.close_unit()
