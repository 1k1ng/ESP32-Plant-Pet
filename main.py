# main.py – ESP32 + ST7789 + MicroPython


import time
from machine import Pin, SPI
import st7789py as st7789
import sensors  # Assuming the updated sensors.py is correctly imported


# Initialize display and other global variables (assuming these are defined)
display = st7789.ST7789(
    spi=SPI(1, baudrate=30_000_000, sck=Pin(18), mosi=Pin(23)),
    dc=Pin(16),
    cs=Pin(5),
    rst=Pin(17),
    width=240,
    height=320,
    backl_pin=None,  # Adjust backlight pin if needed
    backl_active=1   # Backlight active high (adjust as necessary)
)

BLACK = st7789.BLACK
WHITE = st7789.WHITE

previous_state = None


# Define plant profiles (global variable for easy access)
PLANT_PROFILES = {
    "default": {
        "ldr_threshold": 20,
        "soil_moisture_threshold": 10,
        "temperature_max": 30.0,
        "temperature_min": 22.0
    }
}


def determine_plant_state(plant_profile, ldr_percent, soil_percent, temp_c):
    """
    Determines the plant's emotional state based on sensor readings.
    
    :param plant_profile: Dictionary containing threshold values for different emotions.
    :param ldr_percent: Light detection percentage (e.g., 100 for full light).
    :param soil_percent: Soil moisture percentage (e.g., 50 for half wet soil).
    :param temp_c: Temperature in Celsius.
    :return: A string representing the plant's emotional state.
    """
    if ldr_percent < plant_profile["ldr_threshold"]:
        return "sleep"
    elif soil_percent < plant_profile["soil_moisture_threshold"]:
        return "thirsty"
    elif temp_c > plant_profile["temperature_max"]:
        return "hotty"
    elif temp_c < plant_profile["temperature_min"]:
        return "freezy"
    else:
        if 10 <= soil_percent < 90:
            return "savor"
        elif soil_percent >= 90:
            return "happy"


def show_emotion(state, swap_endian=False):
    """
    Displays the corresponding emotion on the ST7789 display.
    
    :param state: The emotional state of the plant (e.g., 'sleep', 'thirsty').
    :param swap_endian: Boolean indicating if byte order needs to be swapped.
    :return: True if the image was successfully displayed, False otherwise.
    """
    try:
        # Assuming _draw_streaming function is defined elsewhere
        _draw_streaming(state + ".bin", swap_endian)
        return True
    except Exception as e:
        print(f"Konnte Bild nicht anzeigen: {state}, Fehler: {e}")
        return False


def _draw_streaming(image_file, swap_endian=False):
    """
    Draws the image from a .bin file on the ST7789 display.
    
    :param image_file: Path to the image file (e.g., 'sleep.bin').
    :param swap_endian: Boolean indicating if byte order needs to be swapped.
    """
    # Open the image file in binary mode
    with open(image_file, "rb") as f:
        image_data = f.read()
    
    # Swap byte order if necessary
    if swap_endian:
        image_data = image_data[::-1]
    
    # Draw the image on the display (assuming display.draw_image exists)
    display.fill(BLACK)  # Clear the screen
    display.blit_buffer(image_data, 0, 0, display.width, display.height)


def main():
    global previous_state
    
    while True:
        try:
            # Read sensor data (ensure this function returns the correct values)
            ldr_percent, soil_percent, temp_c = sensors.read_sensors()
            
            # Determine plant state using the current profile
            plant_profile = PLANT_PROFILES["default"]
            current_state = determine_plant_state(plant_profile, ldr_percent, soil_percent, temp_c)
            
            if current_state != previous_state:
                if show_emotion(current_state, swap_endian=SWAP_ENDIAN):
                    previous_state = current_state
            
            print(f"LDR%: {ldr_percent}, Soil%: {soil_percent}, TempC: {temp_c:.1f}, State: {current_state}")
        
        except Exception as e:
            print(f"Fehler beim Lesen der Sensoren oder Anzeigen des Bildes: {e}")
        
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        display.fill(BLACK)
        print("Beendet.")