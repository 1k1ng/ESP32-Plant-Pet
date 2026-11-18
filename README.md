# 🌿 Plant_Pet_ESP32_D1_Mini

A MicroPython project for the **ESP32-WROOM** that displays the "emotions" of a plant.  
The microcontroller reads light, temperature, and soil moisture, decides on the state  
("sleep", "thirsty", "happy", etc.), and displays the corresponding face on an ST7789 display.

---

## 🔧 Hardware

| Component | Description | Pin on ESP32 |
|----------|---------------|---------------|
| **ST7789 240×320 SPI Display** | 2.0–2.4" SPI display with ST7789 controller | see below |
| **LDR** (Light Sensor) | Voltage divider against 3.3 V | GPIO 32 |
| **LM335** (Temperature Sensor) | Analog output in mV | GPIO 36 |
| **Soil Moisture Sensor** (analog) | 0–3.3 V | GPIO 25 |

### 📺 Display Wiring (ST7789, SPI1)

| Display Pin | ESP32 Pin | Function |
|--------------|-----------|-----------|
| **VCC** | 3V3 | Power Supply |
| **GND** | GND | Ground |
| **SCL (CLK)** | GPIO 18 | SPI Clock |
| **SDA (MOSI)** | GPIO 23 | SPI Data |
| **RES (RESET)** | GPIO 17 | Reset |
| **DC (Data/Command)** | GPIO 16 | Data Control |
| **CS** | GPIO 5 | Chip Select |
| **BL (Backlight)** | 3V3 directly (or PWM pin if dimmable) |

---

## 💾 Firmware Setup

1.  **Flash MicroPython v1.26 or newer onto the ESP32.**
2.  Connect using, for example, [Thonny](https://thonny.org) or [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html).
3.  Upload the following files to the ESP32:
    /main.py
    /sensors.py
    /emotion_static/*.bin
4.  On startup, the ESP32 will automatically display the corresponding emotions.

The `.bin` files are **RGB565-converted PNGs** (240×320), created with your Python converter script.

---

## 🤖 Software Overview

This project is based on and inspired by: [CodersCafeTech/Fyto](https://github.com/CodersCafeTech/Fyto)

| File | Task |
|--------|----------|
| **main.py** | Main logic: read sensors, determine state, display image |
| **sensors.py** | Calibrated sensor values and threshold logic (without IR sensor) |
| **/emotion/emotion_static/** | Contains the converted RGB565 images (e.g., `sleep.bin`, `happy.bin`) |

### States (Emotion Logic)

| Emotion | Description | Condition |
|----------|------------|------------|
| **sleep** | Too dark | `ldr_percent < 20` |
| **thirsty** | Too dry | `soil_percent < 10` |
| **savor** | Normal state | `10 ≤ soil_percent < 90` |
| **happy** | Very moist / just watered | `soil_percent ≥ 90` |
| **hotty** | Too hot | `temp_c > 30 °C` |
| **freezy** | Too cold | `temp_c < 22 °C` |

### ⚖️ License & Credits

This project is a derivative work based on [Fyto](https://github.com/CodersCafeTech/Fyto) by [CodersCafeTech](https://github.com/CodersCafeTech).  
The original work is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License.

**Changes made in this repository:**
* Adapted the codebase to work with MicroPython on an ESP32-WROOM.
* Implemented drivers and logic for the ST7789 display using `.bin` (RGB565) assets.
* Removed the IR sensor logic and adjusted thresholds for LDR, LM335, and capacitive soil moisture sensors.

In accordance with the original license, this project is shared under the same terms and **may not be used for commercial purposes**.  
To view a copy of the full license, visit [CC BY-NC 4.0 Legal Code](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

---


## 🧭 Uploading Files to ESP32 (via USB Terminal)

The official MicroPython tool **mpremote** is used to transfer files to the ESP32.  
This allows you to copy programs, images, and folders directly to the board from your terminal.

### 🔧 Installing mpremote
On your computer (Python required):

```bash
pip install mpremote
```

### 📤 Uploading the files
Replace the port with yours (e.g. `COM3` on Windows, `/dev/ttyUSB0` on Linux):

```bash
# upload the program files
mpremote connect /dev/ttyUSB0 fs cp main.py sensors.py st7789.py vga1_8x16.py vga1_16x32.py :

# upload all images in the folder
mpremote connect /dev/ttyUSB0 fs cp -r emotion_static :
```
