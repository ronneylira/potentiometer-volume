import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from mpd import MPDClient

# Define the ADC channel and gain for the ADS1115
adc_channel = 0

# Initialize the I2C bus and the ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1115(i2c, address=0x49)

# Define volume control parameters
min_volume = 0
max_volume = 100

# Setup MPD client
client = MPDClient()
client.timeout = 10
client.idletimeout = None

# Attempt to connect to MPD
try:
    client.connect("localhost", 6600)
except Exception as e:
    print(f"Failed to connect to MPD: {e}")
    exit(1)

# Main loop
try:
    while True:
        # Read the analog value from the potentiometer
        analog_value = adc.read(adc_channel)

        # Map the analog value to the volume range
        # We are deducting the max_volume because the potentiometer is incorrectly solded
        volume = int(max_volume - (analog_value / 26250) * max_volume)
        volume = max(min_volume, min(volume, max_volume))

        # Set the MPD volume
        try:
            client.setvol(volume)
            print(f"Analog Value: {analog_value}, MPD Volume: {volume}%")
        except Exception as e:
            print(f"Failed to set volume: {e}")
            # Try to reconnect
            try:
                client.disconnect()
            except:
                pass
            try:
                client.connect("localhost", 6600)
            except Exception as reconnect_error:
                print(f"Reconnection failed: {reconnect_error}")

        time.sleep(0.1)

except KeyboardInterrupt:
    client.close()
    client.disconnect()