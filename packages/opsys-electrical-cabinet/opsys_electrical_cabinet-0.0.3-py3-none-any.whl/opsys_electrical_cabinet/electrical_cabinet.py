"""
PLC MODBUS Control API

This module provides a Python class `ElectricalCabinet` for interfacing with a Programmable Logic Controller (PLC) using the MODBUS TCP protocol.

Dependencies:
- pyModbusTCP: Python library for MODBUS TCP communication

Example Usage:
    # Create an instance of ElectricalCabinet with PLC IP address
    cabinet = ElectricalCabinet('192.168.1.100')

    # Read the state of the gimbal interlock
    interlock_state = cabinet.get_gimbal_interlock_state()

    # Set the state of the laser
    cabinet.set_laser_state(1)

    # Read the state of light 1
    light_state = cabinet.get_light_state(1)

    # Set the power state of the gimbal
    cabinet.set_gimbal_power_state(1)

    # Close the TCP connection
    cabinet.close_tcp_conn()

"""
from pyModbusTCP.client import ModbusClient


class ElectricalCabinet():
    """
    A class for interfacing with a Programmable Logic Controller (PLC) using the MODBUS TCP protocol.

    Attributes:
        TCP_CONN (ModbusClient): MODBUS TCP client for communication with the PLC.

    Methods:
        __init__(self, ip_address): Initialize the ElectricalCabinet instance with the given IP address.
        init_tcp_conn(self, ip_address): Open a TCP session with the PLC.
        read_holding_reg(self, reg_adr, reg_num): Read holding registers from the PLC.
        write_holding_reg(self, reg_adr, values): Write values to holding registers on the PLC.
        get_gimbal_interlock_state(self): Get the state of the gimbal interlock.
        set_gimbal_interlock_state(self, value): Set the state of the gimbal interlock.
        get_trx_cover_state(self): Get the state of the TRX cover.
        get_laser_state(self): Get the state of the laser.
        set_laser_state(self, value): Set the state of the laser.
        get_light_state(self, light_num): Get the state of a specific light.
        set_light_state(self, light_num, value): Set the state of a specific light.
        get_gimbal_power_state(self): Get the power state of the gimbal.
        set_gimbal_power_state(self, value): Set the power state of the gimbal.
        get_leds_power_state(self): Get the power state of the LEDs.
        set_leds_power_state(self, value): Set the power state of the LEDs.
        get_spare_power_state(self): Get the power state of the spare.
        set_spare_power_state(self, value): Set the power state of the spare.
        get_hw_tx_state(self): Get the hardware transmission state.
        set_hw_tx_state(self, value): Set the hardware transmission state.
        get_door_interlock_state(self): Get the state of the door interlock.
    """
    
    def __init__(self,):
        """
        Initialize the ElectricalCabinet instance.

        """
        self.TCP_CONN = None
        # self.init_tcp_conn(ip_address)

    def init_tcp_conn(self, ip_address):
        """
        Open a TCP session with the PLC.

        Args:
            ip_address (str): The IP address of the PLC.
        """
        try:
            self.TCP_CONN = ModbusClient(host=ip_address, auto_open=True, auto_close=True)
        except:
            print(self.TCP_CONN)
            print("Error initializing MODBUS TCP connection to PLC")
            raise
        
    def close_tcp_conn(self):
        """
        Close a TCP session with the PLC.
        """
        try:
            self.TCP_CONN.close()
        except:
            print(self.TCP_CONN)
            print("MODBUS TCP connection to PLC is not open!")

    def read_holding_reg(self, reg_adr, reg_num):
        """
        Read holding registers from the PLC.

        Args:
            reg_adr (int): The starting address of the register.
            reg_num (int): The number of registers to read.

        Returns:
            list: The values read from the holding registers.
        """
        try:
            response = self.TCP_CONN.read_holding_registers(reg_adr, reg_num)
            return response
        except:
            print(self.TCP_CONN)
            print("Error reading register from PLC")
            raise

    # values - list of values, starting register from reg_adr
    def write_holding_reg(self, reg_adr, values):
        """
        Write values to holding registers on the PLC.

        Args:
            reg_adr (int): The starting address of the register.
            values (list): The values to write to the registers.
        """
        for val in values:
            if(val):
                val = 1
            else:
                val = 0
        try:
            response = self.TCP_CONN.write_multiple_registers(reg_adr, values)
            return response
        except:
            print(self.TCP_CONN)
            print("Error writing to register on PLC")
            raise

    # PLC SPECIFIC METHODS
    def get_gimbal_interlock_state(self):
        """
        Get the state of the gimbal interlock.

        Returns:
            int: The state of the gimbal interlock (0 or 1).
        """
        return self.read_holding_reg(11,1)[0]

    def set_gimbal_interlock_state(self, value):
        """
        Set the state of the gimbal interlock.

        Args:
            value (int): The value to set the interlock state to (0 or 1).
        """
        self.write_holding_reg(11,[value])

    def get_trx_cover_state(self):
        """
        Get the state of the trx cover.

        Returns:
            int: The state of the trx cover (0 or 1).
        """
        return self.read_holding_reg(3,1)[0]

    def get_laser_state(self):
        """
        Get the state of the laser.

        Returns:
            int: The state of the laser (0 or 1).
        """
        return self.read_holding_reg(12,1)[0]

    def set_laser_state(self, value):
        """
        Set the state of the laser.

        Args:
            value (int): The value to set the laser state to (0 or 1).
        """
        self.write_holding_reg(12,[value])

    # light_num value from [0,1,2]
    def get_light_state(self, light_num):
        """
        Get the state of a specific light.

        Args:
            light_num (int): The index of the light (0, 1, or 2).
            0 - red
            1 - orange
            2 - green
        Returns:
            int: The state of the specified light (0 or 1).
        """
        adr = 0
        if (light_num in [0,1,2]):
            adr = light_num
        return self.read_holding_reg(24 + adr,1)[0]

    def set_light_state(self, light_num, value):
        """
        Set the state of a specific light.

        Args:
            light_num (int): The index of the light (0, 1, or 2).
            0 - red
            1 - orange
            2 - green
            value (int): The value to set the light state to (0 or 1).
        """
        adr = 0
        if (light_num in [0,1,2]):
            adr = light_num
        return self.write_holding_reg(24 + adr,[value])

    def get_gimbal_power_state(self):
        """
        Get the power state of the gimbal.

        Returns:
            int: The power state of the gimbal (0 or 1).
        """
        return self.read_holding_reg(8,1)[0]

    def set_gimbal_power_state(self, value):
        """
        Set the power state of the gimbal.

        Args:
            value (int): The value to set the gimbal power state to (0 or 1).
        """
        self.write_holding_reg(8,[value]) 

    def get_leds_power_state(self):
        """
        Get the power state of the LEDs.

        Returns:
            int: The power state of the LEDs (0 or 1).
        """
        return self.read_holding_reg(10,1)[0]

    def set_leds_power_state(self, value):
        """
        Set the power state of the LEDs.

        Args:
            value (int): The value to set the LEDs power state to (0 or 1).
        """
        self.write_holding_reg(10,[value]) 

    def get_spare_power_state(self):
        """
        Get the spare power state.

        Returns:
            int: The spare power state (0 or 1).
        """
        return self.read_holding_reg(9,1)[0]

    def set_spare_power_state(self, value):
        """
        Set the power state of the spare.

        Args:
            value (int): The value to set the spare power state to (0 or 1).
        """
        self.write_holding_reg(9,[value]) 

    def get_hw_tx_state(self):
        """
        Get the hardware trx state.

        Returns:
            int: The hardware trx state (0 or 1).
        """
        return self.read_holding_reg(30,1)[0]

    def set_hw_tx_state(self, value):
        """
        Set the hardware trx state.

        Args:
            value (int): The value to set the hardware trx state to (0 or 1).
        """
        self.write_holding_reg(30,[value]) 

    def get_door_interlock_state(self):
        """
        Get the state of the trx cover.

        Returns:
            int: The state of the trx cover (0 or 1).
        """
        return self.read_holding_reg(5,1)[0]
