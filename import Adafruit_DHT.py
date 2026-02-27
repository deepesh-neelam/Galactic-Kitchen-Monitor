import time
import random

# ========== MOCK MODULES FOR WINDOWS TESTING ==========

class MockAdafruit_DHT:
    DHT11 = 11
    
    @staticmethod
    def read(sensor, pin):
        # Simulate sensor readings
        temp = random.uniform(20, 35)
        humidity = random.uniform(30, 80)
        return humidity, temp

Adafruit_DHT = MockAdafruit_DHT()

class MockSpiDev:
    def __init__(self):
        self.max_speed_hz = 1350000
    
    def open(self, bus, device):
        pass
    
    def xfer2(self, data):
        # Simulate ADC reading (0-1023)
        return [0, random.randint(0, 3), random.randint(0, 255)]

class MockLED:
    def __init__(self, pin):
        self.pin = pin
        self.state = False
    
    def on(self):
        self.state = True
        print(f"✅ LED (GPIO {self.pin}) turned ON")
    
    def off(self):
        self.state = False
        print(f"⚫ LED (GPIO {self.pin}) turned OFF")

# ========== SENSOR SETUP ==========

# DHT Setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# LED Setup
status_led = MockLED(17)

# SPI Setup for MCP3008
spi = MockSpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# ========== GALACTIC LOGIC ==========

def check_mission_status(temp, humidity, solar_value):
    
    if temp > 35:
        return "🔥 Overheat Alert! Reduce kitchen load!"
    
    elif humidity < 30:
        return "💧 Hydroponics Dry! Increase water supply!"
    
    elif solar_value < 200:
        return "⚡ Low Solar Power! Switch to battery!"
    
    else:
        return "🚀 Flavortown Achieved! Meal Ready!"

# ========== MAIN LOOP ==========

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    solar = read_adc(0)

    if humidity is not None and temperature is not None:
        status = check_mission_status(temperature, humidity, solar)

        print("🌡 Temp:", temperature, "°C")
        print("💧 Humidity:", humidity, "%")
        print("☀ Solar Level:", solar)
        print("Status:", status)
        print("---------------------------")

        if "Flavortown Achieved" in status:
            status_led.on()
        else:
            status_led.off()

    else:
        print("Sensor failure. Check wiring.")

    time.sleep(5)