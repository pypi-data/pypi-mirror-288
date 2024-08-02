

# MH410D by NekoSensors

A Python library for interfacing with the MH-410D CO2 sensor via UART.

Sensor Datasheet (+ Protocol) - [MH-410D.PDF](docs%2FMH-410D.PDF)

![image.png](__assets__%2Fimage.png)

## Installation

You can install the library via pip:

```bash
pip install MH410D
```

## Usage

Here is an example of how to use the `MH410D` library:

```python
from MH410D import MH410D_CO2

# Create an instance of the sensor
sensor = MH410D_CO2(port='COM3', baudrate=9600, timeout=2)

# Read gas concentration
concentration_ppm = sensor.read_gas_concentration()
if concentration_ppm is not None:
    print(f"Gas concentration: {concentration_ppm} ppm")
    print(f"Gas concentration: {sensor.ppm_to_percent(concentration_ppm)} %")

    # Example conversion to mg/m3 for carbon dioxide (CO2), molar mass 44 g/mol
    concentration_mg_m3 = sensor.ppm_to_mg_m3(concentration_ppm, molar_mass=44)
    print(f"Gas concentration: {concentration_mg_m3} mg/m3")

# Calibrate the sensor
sensor.calibrate_zero()
sensor.calibrate_span()

# Close the connection
sensor.close()
```

## Features

- **Read Gas Concentration**: Read CO2 concentration in ppm from the MH-410D sensor.
- **Calibrate Sensor**: Calibrate the zero and span points of the sensor.
- **Convert Units**: Convert gas concentration from ppm to percentage and mg/m3.

## API Reference

### `MH410D_CO2`

#### `__init__(self, port='COM3', baudrate=9600, timeout=2)`

Initializes the serial connection with the specified parameters.

- `port` (str): Port name to which the sensor is connected (default 'COM3').
- `baudrate` (int): Data transmission speed (default 9600).
- `timeout` (int): Timeout for read operations (default 2 seconds).

#### `read_gas_concentration(self)`

Sends a command to read gas concentration and returns the value.

- **Returns**: Gas concentration in ppm, or `None` if reading failed.

#### `calibrate_zero(self)`

Sends a command to calibrate the sensor zero point.

- **Returns**: `True` if calibration is successful, otherwise `False`.

#### `calibrate_span(self)`

Sends a command to calibrate the sensor span point.

- **Returns**: `True` if calibration is successful, otherwise `False`.

#### `ppm_to_percent(self, ppm)`

Converts ppm to percentage.

- `ppm` (int): Value in ppm.
- **Returns**: Value in percentage.

#### `ppm_to_mg_m3(self, ppm, molar_mass, temperature=25, pressure=101325)`

Converts ppm to mg/m3.

- `ppm` (int): Value in ppm.
- `molar_mass` (float): Molar mass of the gas in grams per mole.
- `temperature` (float): Temperature in degrees Celsius (default 25).
- `pressure` (float): Pressure in Pascals (default 101325 Pa).
- **Returns**: Value in mg/m3.

#### `close(self)`

Closes the serial connection.


### Out Another Projects:

https://github.com/NekoRMD/NekoRMD - Control MyActuator RMD X8-PRO using Python by CAN

https://github.com/K-Lab-Students/REIS_PCB - PBC library

