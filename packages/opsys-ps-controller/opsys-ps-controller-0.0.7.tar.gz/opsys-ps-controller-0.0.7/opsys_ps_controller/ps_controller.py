from .ps_abstract import PsAbstract
from .ps_configs import *


class PsController(PsAbstract):
    """
    Power Supply controller

    """

    def __init__(self,
                 baudrate=TdkZupConfig.BAUDRATE,
                 delay=TdkZupConfig.DELAY,
                 address=TdkZupConfig.ADDRESS,
                 ps_type=PsTypes.TDK_Z_UP):
        """
        constructor

        Args:
            baudrate (int, optional): COMs baud rate
            delay (float, optional): delay time between serial
                                     interface commands
            address (int, optional): device address
            ps_type (str, optional): device type/model
        """
        self._baudrate = baudrate
        self._delay = delay
        self._address = address
        self._ps_type = ps_type
        self.ps_controller = None

    def init_connection(self):
        """
        Scan COM ports to find ATEN related

        Returns:
            bool: connection to PS status
            
        Raises:
            ValueError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            from .tdk_zup_controller import TdkZupController

            self.ps_controller = TdkZupController(self._baudrate,
                                                   self._delay,
                                                   self._address,
                                                   TdkZupConfig.BUFFER_SIZE)
            is_connected = self.ps_controller.init_connection()
            
        elif self._ps_type == PsTypes.TDK_Z:
            from .tdk_z_controller import TdkZController
            
            self.ps_controller = TdkZController(self._address)
            is_connected = True
            
        else:
            raise ValueError("Can't find device type")
        
        self.ps_controller.set_mode(is_remote=True)
        
        return is_connected

    def disconnect(self):
        """
        Disconnect from serial connection
        """
        self.ps_controller.disconnect()

    def ps_on(self):
        """
        Set power on
        """
        self.ps_controller.ps_on()

    def ps_off(self):
        """
        Set power off
        """
        self.ps_controller.ps_off()
            
    def ps_reset(self, reset_delay=1, wait_for_user_interaction_callback=None):
        """
        Reset power supply

        Args:
            reset_delay (int, optional): delay time after reset. Defaults to 1.
            wait_for_user_interaction_callback (Callable, optional): Callback object instance. 
                                                                     Defaults to None.
        """
        self.ps_controller.ps_reset(reset_delay, wait_for_user_interaction_callback)

    def get_current(self):
        """
        Read power supply current

        Returns:
            float: electrical current value
        """
        return self.ps_controller.get_current()
    
    def get_voltage(self):
        """
        Read power supply voltage

        Returns:
            float: voltage value
        """
        return self.ps_controller.get_voltage()
    
    def set_current(self, current):
        """
        Set power supply current

        Args:
            current (float): electrical current value
        """
        print(f'Set current to: {current}')
        self.ps_controller.set_current(current)
    
    def set_voltage(self, voltage):
        """
        Set power supply voltage

        Args:
            voltage (float): voltage value
        """
        print(f'Set voltage to: {voltage}')
        self.ps_controller.set_voltage(voltage)

    def clear_device_status(self):
        """
        Clear device status
        """
        self.ps_controller.clear_device_status()
            
    def get_system_error(self):
        """
        Read system error if exists

        Returns:
            str: system error
        """
        return self.ps_controller.get_system_error()
    
    def get_lan_ip_address(self):
        """
        Read PS IP address

        Raises:
            NotImplementedError

        Returns:
            str: IP address
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_lan_ip_address()
        
    def get_lan_host_name(self):
        """
        Read ps host name

        Raises:
            NotImplementedError

        Returns:
            str: LAN hostname
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_lan_host_name()
        
    def reset_device_configs(self):
        """
        Read PS configurations

        Raises:
            NotImplementedError

        Returns:
            str: IP address
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.reset_device_configs()
        
    def get_device_id(self):
        """
        Read device id

        Returns:
            str: device id
        """
        return self.ps_controller.get_device_id()

    def is_remote(self):
        """
        Check if remote mode is active or not

        Returns:
            bool: Remote mode status (enabled/disabled)
        """
        return self.ps_controller.is_remote()

    def set_mode(self, is_remote):
        """
        Set operation mode - remote or local

        Args:
            is_remote (bool): True for remote mode activation
                              False for remote mode deactivation
        """
        print('Set remote mode')
        return self.ps_controller.set_mode(is_remote)

    def set_ps_address(self, address):
        """
        Set PS address ID number
        
        Raises:
            NotImplementedError

        Args:
            address (int): address ID number, between 1 and 9
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            return self.ps_controller.set_ps_address(address)

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def is_on(self):
        """
        Checking if the PS is on (output voltage exists)

        Returns:
            bool: PS On/Off status
        """
        return self.ps_controller.is_on()

    def set_voltage_limit(self, max_voltage):
        """
        Set voltage limit

        Args:
            max_voltage (float): max voltage value
        """
        print(f'Set voltage limit to: {max_voltage}')
        self.ps_controller.set_voltage_limit(max_voltage)
        