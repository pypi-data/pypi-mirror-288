import unittest
from unittest.mock import patch, MagicMock
from opsys_ps_controller.tdk_z_controller import TdkZController


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

    @ patch.object(TdkZController, 'init_connection')
    def test_init_connection(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.init_connection()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'get_device_id')
    def test_get_device_id(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_device_id()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'disconnect')
    def test_disconnect(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.disconnect()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'ps_on')
    def test_ps_on(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.ps_on()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'ps_off')
    def test_ps_off(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.ps_off()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'reset_device_configs')
    def test_reset_device_configs(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.reset_device_configs()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'get_current')
    def test_get_current(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_current()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'set_current')
    def test_set_current(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        current = 2
        ps_conn.set_current(current=current)
        ps_mock.assert_called_once_with(current=2)

    @ patch.object(TdkZController, 'get_voltage')
    def test_get_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_voltage()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'set_voltage')
    def test_set_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        voltage = 12
        ps_conn.set_voltage(voltage=voltage)
        ps_mock.assert_called_once_with(voltage=12)

    @ patch.object(TdkZController, 'is_remote')
    def test_is_remote(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.is_remote()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'get_system_error')
    def test_get_system_error(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_system_error()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'get_lan_ip_address')
    def test_get_lan_ip_address(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_lan_ip_address()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'get_lan_host_name')
    def test_get_lan_host_name(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.get_lan_host_name()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'ps_reset')
    def test_ps_reset(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.ps_reset()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'is_on')
    def test_is_on(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        ps_conn.is_on()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'set_voltage_limit')
    def test_set_voltage_limit(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR')
        voltage_limit = 12.5
        ps_conn.set_voltage_limit(voltage_limit)
        ps_mock.assert_called_once_with(12.5)


if __name__ == '__main__':
    unittest.main()
