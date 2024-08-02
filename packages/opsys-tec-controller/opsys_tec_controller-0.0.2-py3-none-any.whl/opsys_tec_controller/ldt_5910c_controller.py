from .tec_abstract import TecAbstract
import pyvisa
import pandas as pd
import time
import os


class Idt5910cController(TecAbstract):
    """
    IDT-5910C Device Interface
    """
    _sleep_time = 0.3

    def __init__(self,
                 device_address,
                 lut_filepath):
        """
        constructor

        Args:
            device_address (str): Device address
            lut_filepath (str): Resistance to temperature LUT
        """
        self._device_address = device_address
        self._resistance_to_temp_db = None
        self._filepath = lut_filepath
        
        self.rm = pyvisa.ResourceManager()
        
    def load_lut(self, lut_filepath=None):
        """
        Load temperature to resistance LUT

        Args:
            lut_filepath (str, optiona): Resistance to temperature LUT path.
                                         Defaults to None.
        """
        self._filepath = self._filepath if lut_filepath is None else lut_filepath
        self._resistance_to_temp_db = pd.read_csv(self._filepath)
        self._min_resistance_thresholds = list(self._resistance_to_temp_db['Min'][1:].astype('float'))
        self._max_resistance_thresholds = list(self._resistance_to_temp_db['Max'][1:].astype('float'))
        
    def connect(self):
        """
        Connect to device
        
        Returns:
            bool: connection status.
                  True if conncted, else False.
        """
        # load temp/resistance conversion table
        if self._resistance_to_temp_db is None:
            self.load_lut()

        try:
            self.device = self.rm.open_resource(self._device_address)
            print(f'Connected to device: {self.device}')
            return True
        except Exception as e:
            print(f'Failed to connect to device: {self._device_address}. {e}')
            return False
            
    def disconnect(self):
        """
        Disconnect from device
        """
        self.device.close()
        
    def _send_command(self, command):
        """
        Send command to device

        Args:
            command (str): input command
        """
        self.device.write(command)
    
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

    def device_on(self):
        """
        Set power on
        """
        self._send_command(':OUTPut 1')

    def device_off(self):
        """
        Set power off
        """
        self._send_command(':OUTPut 0')
        
    def device_reset(self):
        """
        Reset TEC
        """
        self.device_off()
        time.sleep(self._sleep_time)
        self.device_on()
    
    def set_temperature(self, temperature):
        """
        Set temperature value, using corresponding
        resistance value

        Args:
            temperature (int): Temperature setpoint.
        """
        table_row = self._resistance_to_temp_db[self._resistance_to_temp_db['Temp'] == str(temperature)]
        try:
            resistance = float(table_row['Nom'])
            
            self.set_resistance(resistance)
        except Exception as e:
            print(f'Input value is out of defined range - {temperature}. {e}')
    
    def get_temperature(self):
        """
        Get current temperature value
        
        Returns:
            float: temperature
        """
        try:
            resistance = self.get_resistance()
            min_temperature = [self._resistance_to_temp_db['Temp'][row] for row, res in enumerate(self._min_resistance_thresholds) if res < resistance][0]
            max_temperature = [self._resistance_to_temp_db['Temp'][row] for row, res in enumerate(self._max_resistance_thresholds) if res < resistance][0]
            
            temperature = (float(min_temperature) + float(max_temperature)) / 2  # take mean of two possible ranges
        except Exception as e:
            print(f'Error reading temperature for R={resistance} (ohm)!. {e}')
            temperature = -999
        
        return temperature

    def scan_temperature(self, scan_time):
        """
        Scan temperature value
        
        Args:
            scan_time (float): Scanning time in sec.
        
        Returns:
            list: temperature samples list
        """
        self._temp_samples = []
        start_time = time.time()
        
        while (time.time() - start_time) <= scan_time:
            self._temp_samples.append(self.get_temperature())
            # wait before next sample
            time.sleep(self._sleep_time / 10)
            
        print('Temperature scanning stopped!')
        return self._temp_samples
        
    def is_on(self):
        """
        Checking if the device is on (output voltage exists)

        Returns:
            bool: On/Off status
        """
        response = self._query('OUTput?')
        return True if response == 'ON' else False

    def get_system_error(self):
        """
        Get system errors

        Returns:
            str: system errors info
        """
        return self._query(':ERRors?')

    def get_device_id(self):
        """
        Read device id
        
        Returns:
            bool: device ID string
        """
        return self._query('*IDN?')

    def reset_device_configs(self):
        """
        Reset device configurations
        """
        self._send_command(':*RST')
        
    def get_current_lower_limit(self):
        """
        Get current lower limit

        Returns:
            float: min current value (A)
        """
        return float(self._query(':LIMit:ITE:LOw?'))

    def set_current_lower_limit(self, limit):
        """
        Set current lower limit

        Args:
            limit (float): min current value (A)
        """
        self._send_command(f':LIMit:ITE:LOw {limit}')
        
    def get_current_higher_limit(self):
        """
        Get current higher limit

        Returns:
            float: max current value (A)
        """
        return float(self._query(':LIMit:ITE:HIgh?'))

    def set_current_higher_limit(self, limit):
        """
        Set current higher limit

        Args:
            limit (float): max current value (A)
        """
        self._send_command(f':LIMit:ITE:HIgh {limit}')
        
    def get_sensor_lower_protection(self):
        """
        Get sensor lower protection limit

        Returns:
            float: lower limit (resistance|µA|mV)
        """
        return float(self._query(':LIMit:SENsor:LOw?'))

    def set_sensor_lower_protection(self, limit):
        """
        Set sensor lower protection limit

        Args:
            limit (float): lower limit (resistance|µA|mV)
        """
        self._send_command(f'LIMit:SENsor:LOw {limit}')
        
    def get_sensor_higher_protection(self):
        """
        Get sensor higher protection limit

        Returns:
            float: higher limit (resistance|µA|mV)
        """
        return float(self._query(':LIMit:SENsor:HIgh?'))

    def set_sensor_higher_protection(self, limit):
        """
        Set sensor higher protection limit

        Args:
            limit (float): higher limit (resistance|µA|mV)
        """
        self._send_command(f'LIMit:SENsor:HIgh {limit}')
        
    def get_sensor_lower_temperature(self):
        """
        Get sensor lower temperature limit

        Returns:
            float: lower limit (degrees)
        """
        return float(self._query('LIMit:Temp:LOw?'))
        
    def set_sensor_lower_temperature(self, limit):
        """
        Set sensor lower temperature limit

        Args:
            limit (float): lower limit (degrees)
        """
        self._send_command(f'LIMit:Temp:LOw {limit}')
        
    def get_sensor_higher_temperature(self):
        """
        Get sensor higher temperature limit

        Returns:
            float: lower limit (degrees)
        """
        return float(self._query(':LIMit:Temp:HIgh?'))

    def set_sensor_higher_temperature(self, limit):
        """
        Set sensor higher temperature limit

        Args:
            limit (float): higher limit (degrees)
        """
        self._send_command(f'LIMit:Temp:HIgh {limit}')
        
    def get_sensor_type(self):
        """
        Get selected sensor type (ICI|ICV...)
        ref. pg.63 in user manual, <SENsor> section
        
        Returns:
            str: sensor type
        """
        return self._query(':SENsor?')
    
    def set_sensor_type(self, sensor_type):
        """
        Set sensor type (ICI|ICV...)
        ref. pg.63 in user manual, <SENsor> section
        
        Args:
            sensor_type (str): sensor type
        """
        self._send_command(f':SET:SENsor {sensor_type}')

    def get_sensor_value(self):
        """
        Get sensor measured value R, A, mV
        
        Retruns:
            float: measured value
        """
        try:
            print(f'Sensor type is: {self.get_sensor_type()}')
            result = float(self._query('MEASure:SENsor?'))
        except Exception as e:
            print(f'Error reading sensor, {result}. {e}')
            result = 'Error'

        return result
    
    def get_resistance(self):
        """
        Get output cable resistance
        
        Retruns:
            float: cable resistance (ohm)
        """
        try:
            resistance = float(self._query(':CABLER?'))
        except Exception as e:
            print(f'Error reading resistance, R={resistance}. {e}')
            resistance = 'Error'

        return resistance
    
    def set_resistance(self, resistance):
        """
        Get output cable resistance
        
        Args:
            resistance (float): resistance value
        """
        self._send_command(f':CABLER {resistance}')
