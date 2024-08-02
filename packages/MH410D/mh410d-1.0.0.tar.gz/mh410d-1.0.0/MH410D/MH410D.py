from BaseSensor import BaseSensor



class MH410D_CO2(BaseSensor):
    def calculate_checksum(self, command):
        """
        Calculates the checksum for the command.

        :param command: List of command bytes.
        :return: Checksum.
        """
        return (0xFF - (sum(command[1:8]) % 256) + 1) & 0xFF

    def read_gas_concentration(self):
        """
        Sends a command to read gas concentration and returns the value.

        :return: Gas concentration in ppm, or None if reading failed.
        """
        command = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.send_command(command)
        if response and len(response) == 9:
            gas_concentration = response[2] * 256 + response[3]
            return gas_concentration
        else:
            print("Failed to read gas concentration")
            return None

    def calibrate_zero(self):
        """
        Sends a command to calibrate the sensor zero point.

        :return: True if calibration is successful, otherwise False.
        """
        command = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.send_command(command)
        if response and len(response) == 9:
            print("Sensor zero point calibration successful")
            return True
        else:
            print("Failed to calibrate sensor zero point")
            return False

    def calibrate_span(self):
        """
        Sends a command to calibrate the sensor span point.

        :return: True if calibration is successful, otherwise False.
        """
        command = [0xFF, 0x01, 0x88, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.send_command(command)
        if response and len(response) == 9:
            print("Sensor span point calibration successful")
            return True
        else:
            print("Failed to calibrate sensor span point")
            return False

    def ppm_to_percent(self, ppm):
        """
        Converts ppm to percentage.

        :param ppm: Value in ppm.
        :return: Value in percentage.
        """
        return ppm / 10000

    def ppm_to_mg_m3(self, ppm, molar_mass, temperature=25, pressure=101325):
        """
        Converts ppm to mg/m3.

        :param ppm: Value in ppm.
        :param molar_mass: Molar mass of the gas in grams per mole.
        :param temperature: Temperature in degrees Celsius (default 25).
        :param pressure: Pressure in Pascals (default 101325 Pa).
        :return: Value in mg/m3.
        """
        R = 8.314  # Universal gas constant, J/(mol·K)
        T = temperature + 273.15  # Temperature in Kelvin
        return (ppm * molar_mass * pressure) / (R * T * 1000)
