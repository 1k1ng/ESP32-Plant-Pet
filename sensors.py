"""
sensors.py – Kalibrierte Sensorfunktionen für ESP32-WROOM
Liest LDR (Licht), Bodenfeuchte und LM335 (Temperatur) aus
und liefert normierte Werte in Prozent bzw. Grad Celsius.
"""

import time
from machine import Pin, ADC

# --- Pin mapping -------------------------------------------------------------
LM335_ADC = ADC(Pin(36))   # ADC1_CH0
LDR_ADC = ADC(Pin(32))     # ADC1_CH4
SOIL_ADC = ADC(Pin(25))    # ADC2_CH8  (bei WLAN ggf. auf ADC1-Pin umlegen)

for adc in (LM335_ADC, LDR_ADC, SOIL_ADC):
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)

# --- Calibration constants ---------------------------------------------------
ADC_RESOLUTION = 4095
VREF_MV = 3300
LM335_MV_PER_K = 10.0
LM335_OFFSET_K = 273.15

LDR_MAX_BRIGHTNESS = 3800
LDR_MIN_BRIGHTNESS = 400
WET_SOIL_MOISTURE = 1150
DRY_SOIL_MOISTURE = 2820


def map_range(value, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return out_min
    scaled = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(out_min, min(out_max, int(scaled)))


def read_sensors():
    """
    Reads data from the light, temperature, and soil moisture sensors.

    :return: A tuple containing ldr_percent (int), soil_percent (int), and temp_c (float).
    """
    # Simulated sensor readings
    # Replace these with actual sensor reading code in your implementation

    ldr_raw = 1000
    soil_raw = 1500
    lm335_raw = 2048
    ldr_percent = map_range(ldr_raw, LDR_MIN_BRIGHTNESS, LDR_MAX_BRIGHTNESS, 0, 100)
    soil_percent = map_range(soil_raw, DRY_SOIL_MOISTURE, WET_SOIL_MOISTURE, 0, 100)

    lm335_mv = lm335_raw * VREF_MV / ADC_RESOLUTION
    temp_c = (lm335_mv / LM335_MV_PER_K) - LM335_OFFSET_K

    return ldr_percent, soil_percent, temp_c


def choose_state(ldr_percent, soil_percent, temp_c):
    """Bestimmt den Pflanzenzustand anhand der Sensorwerte."""
    if ldr_percent < 20:
        return "sleep"
    if soil_percent < 10:
        return "thirs"
    if 10 <= soil_percent < 90:
        return "savor"
    if soil_percent >= 90:
        return "happy"
    if temp_c > 30:
        return "hotty"
    if temp_c < 22:
        return "freez"
    return "happy"


def main():
    """Einfacher Testmodus: gibt alle Werte seriell aus."""
    print("Starte Sensorschleife – Werte alle 500 ms.")
    while True:
        ldr, soil, temp_c = read_sensors()
        state = choose_state(ldr, soil, temp_c)
        print(
            "LDR%:", ldr,
            "| Soil%:", soil,
            "| TempC:", round(temp_c, 1),
            "| Zustand:", state,
        )
        time.sleep(0.5)


if __name__ == "__main__":
    main()

