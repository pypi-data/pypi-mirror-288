import serial
import time

class BaseSensor:
    def __init__(self, port='COM3', baudrate=9600, timeout=2):
        """
        Initializes serial connection with specified parameters.

        :param port: Port name to which the sensor is connected (default 'COM3').
        :param baudrate: Data transmission speed (default 9600).
        :param timeout: Timeout for read operations (default 2 seconds).
        """
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        if self.ser.is_open:
            print("Serial port opened successfully")

    def send_command(self, command):
        """
        Sends a command to the sensor and receives a response.

        :param command: List of command bytes.
        :return: Response from the sensor as bytes.
        """
        checksum = self.calculate_checksum(command)
        command.append(checksum)
        self.ser.write(bytearray(command))
        print(f"Command sent: {command}")
        time.sleep(2)  # Increased response wait time
        response = self.ser.read(9)
        print(f"Response: {response}")
        return response

    def calculate_checksum(self, command):
        """
        Calculates the checksum for the command.

        :param command: List of command bytes.
        :return: Checksum.
        """
        raise NotImplementedError("This method must be implemented in a subclass")

    def close(self):
        """
        Closes the serial connection.
        """
        self.ser.close()
        print("Serial port closed")