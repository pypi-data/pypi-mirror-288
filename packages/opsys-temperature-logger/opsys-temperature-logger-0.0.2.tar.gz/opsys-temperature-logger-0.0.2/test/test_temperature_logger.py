import unittest
from unittest.mock import patch, MagicMock
from opsys_temperature_logger.temperature_logger import TemperatureLogger


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(TemperatureLogger, 'connect')
    def test_connect(self, pico_mock: MagicMock):
        pico = TemperatureLogger()
        pico.connect()
        pico_mock.assert_called_once_with()

    @ patch.object(TemperatureLogger, 'set_channel')
    def test_set_channel(self, pico_mock: MagicMock):
        pico = TemperatureLogger()
        channel = 3
        pico.set_channel(channel=channel)
        pico_mock.assert_called_once_with(channel=3)

    @ patch.object(TemperatureLogger, 'read_temperature')
    def test_read_temperature(self, pico_mock: MagicMock):
        pico = TemperatureLogger()
        channel = 3
        pico.read_temperature(channel=channel)
        pico_mock.assert_called_once_with(channel=3)

    @ patch.object(TemperatureLogger, 'close_connection')
    def test_close_connection(self, pico_mock: MagicMock):
        pico = TemperatureLogger()
        pico.close_connection()
        pico_mock.assert_called_once_with()
