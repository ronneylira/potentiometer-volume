# Potentiometer Volume Control for MPD

A Python application that controls Music Player Daemon (MPD) volume using a potentiometer connected via an ADS1115 ADC module.

## Overview

This project reads analog values from a potentiometer using an ADS1115 16-bit ADC and maps those values to control the volume of MPD (Music Player Daemon) running on your system. Perfect for building a physical volume control interface for your music server.

## Hardware Requirements

- Raspberry Pi (or compatible single-board computer)
- ADS1115 16-bit ADC module
- Potentiometer (connected to ADS1115)
- I2C connection between Raspberry Pi and ADS1115

## Software Requirements

- Python 3.x
- MPD (Music Player Daemon) running on localhost:6600
- I2C enabled on Raspberry Pi

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd potentiometer-volume
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Enable I2C on Raspberry Pi (if not already enabled):
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > I2C > Enable
   ```

4. Ensure MPD is installed and running:
   ```bash
   sudo apt-get install mpd
   sudo systemctl start mpd
   sudo systemctl enable mpd
   ```

## Configuration

The ADS1115 is configured with the I2C address `0x49` by default. If your ADC uses a different address, modify line 13 in `main.py`:

```python
adc = ADS.ADS1115(i2c, address=0x49)  # Change 0x49 to your address
```

Volume range is set to 0-100% by default. You can adjust these values in `main.py`:

```python
min_volume = 0
max_volume = 100
```

**Note:** The code includes a correction for a reversed potentiometer wiring (see line 39). If your potentiometer is wired correctly, you may need to adjust the volume calculation.

## Usage

Run the script:
```bash
python main.py
```

The script will:
- Connect to MPD on localhost:6600
- Continuously read the potentiometer value
- Map the analog reading to volume (0-100%)
- Update MPD volume accordingly
- Print the current analog value and volume percentage

Press `Ctrl+C` to stop the script.

## Troubleshooting

- **Connection to MPD fails**: Ensure MPD is running and accessible on port 6600:
  ```bash
  sudo systemctl status mpd
  ```

- **ADC not detected**: Check I2C connection and address:
  ```bash
  sudo i2cdetect -y 1
  ```

- **Volume not changing**: Verify the potentiometer is properly connected to the ADS1115 and the ADC channel matches your wiring (default is channel 0).

## Dependencies

- `adafruit-circuitpython-ads1x15` - ADS1115 ADC driver
- `python-mpd2` - MPD client library
- `Adafruit-Blinka` - CircuitPython library for Raspberry Pi
- Other supporting libraries (see `requirements.txt`)

## License

This project is licensed under the MIT License.

