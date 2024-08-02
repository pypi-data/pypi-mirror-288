import time
import pyvisa
from .ps_abstract import PsAbstract


class TdkZController(PsAbstract):
    """
    TDK Lambda LAN Power Supply controller

    """

    def __init__(self, address):
        self._address = address
        self.device = None
        self.rm = pyvisa.ResourceManager()
    
    def init_connection(self):
        """
        Connect to PS

        Returns:
            bool: connection to PS status
        """
        try:
            self.device = self.rm.open_resource(self._address)
            print(f'Connected to device: {self._address}')
            return True
        except Exception as e:
            print(f'Failed to connect to device: {self._address}. {e}')
            return False

    def _send_command(self, command):
        """
        Send command to device

        Args:
            command (str): input command
        """
        self.device.write(command)

    def _read_response(self):
        response = self.device.read()
        return response.strip()
    
    def _query(self, command):
        """
        Get query result from device

        Args:
            command (str): query command

        Returns:
            str: query result
        """
        self.device.write(command)
        response = self.device.read()
        return response.strip()

    def get_device_id(self):
        """
        Read device id
        """
        self._send_command('*IDN?')
        return self._read_response()
   
    def reset_device_configs(self):
        """
        Reset PS configurations
        """
        self._send_command(':*RST')
   
    def clear_device_status(self):
        """
        Clear device status
        """
        self._send_command(':*CLS')
        
    def is_remote(self):
        """
        Check if remote mode is active or not

        Returns:
            bool: Remote mode status (enabled/disabled)
        """
        current_mode = self._query('RMT?')
        if current_mode == "REM":
            print('The PS is in remote mode')
            return True
        else:
            print('The PS is not in remote mode')
        return False
    
    def set_mode(self, is_remote):
        """
        Set operation mode - remote or local

        Args:
            is_remote (bool): True for remote mode activation
                              False for remote mode deactivation
        """
        if is_remote:
            self._send_command('SYST:REM REM')
        else:
            self._send_command('SYST:REM LOC')
   
    def get_system_error(self):
        """
        Get system errors

        Returns:
            str: system errors info
        """
        return self._query('SYST:ERROR?')
 
    def get_lan_ip_address(self):
        """
        Get device IP

        Returns:
            str: PS IP
        """
        return self._query('SYSTem:COMM:LAN:IP?')
 
    def get_lan_host_name(self):
        """
        Get device hostname

        Returns:
            str: PS hostname
        """
        return self._query('SYST:COMM:LAN:HOST?')
   
    def set_voltage(self, voltage):
        """
        Set power supply voltage

        Args:
            voltage (float): voltage value
        """
        self._send_command(f':VOLT {voltage}')
 
    def set_current(self, current):
        """
        Set power supply current

        Args:
            current (float): electrical current value
        """
        self._send_command(f':CURR {current} MA')
 
    def ps_on(self):
        """
        Set power on
        """
        self._send_command(':OUTP:STAT ON')
        
    def ps_off(self):
        """
        Set power off
        """
        self._send_command(':OUTP:STAT OFF')
        
    def ps_reset(self, reset_delay=1, wait_for_user_interaction_callback=None):
        """
        Reset power supply

        Args:
            reset_delay (int, optional): delay time after reset. Defaults to 1.
            wait_for_user_interaction_callback (Callable, optional): Callback object instance. 
                                                                     Defaults to None.
        """
        try:
            self.ps_off()
            print("Please wait while the system is restart...")
            self.ps_on()
            time.sleep(reset_delay)
        except:
            if wait_for_user_interaction_callback is not None:
                wait_for_user_interaction_callback(
                    "Power cycle the system, press 'OK' after system is ready")
            else:
                input("Power cycle the system, press 'OK' after system is ready\n")
                
    def is_on(self):
        """
        Checking if the PS is on (output voltage exists)

        Returns:
            bool: PS On/Off status
        """
        self._send_command('OUT?')
        response = self._read_response()
        return True if response == 'ON' else False
 
    def get_voltage(self):
        """
        Read power supply voltage

        Returns:
            float: voltage value
        """
        self._send_command('MEAS:VOLT?')
        return round(float(self._read_response()), 2)
 
    def get_current(self):
        """
        Read power supply current

        Returns:
            float: electrical current value
        """
        self._send_command('MEAS:CURR?')
        return round(float(self._read_response()), 2)
 
    def disconnect(self):
        """
        Disconnect from serial connection
        """
        self.device.close()

    def set_voltage_limit(self, max_voltage):
        """
        Set voltage limit

        Args:
            max_voltage (float): max voltage value
        """
        self._send_command(f':OVP {max_voltage}')
