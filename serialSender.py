import serial
import sys
import time

# Serial port settings (adjust the port and baudrate to match your Arduino)
SERIAL_PORT = "COM13"  # Change this for Linux/macOS: "/dev/ttyUSB0" or "/dev/ttyACM0"
BAUD_RATE = 115200     # Common baud rates: 9600, 115200

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    print("Connected to Arduino")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Function to send GCode commands
def send_gcode(file_path):
    with open(file_path, "r") as file:
        for line in file:
            gcode = line.strip()  # Remove extra spaces and newlines
            if not gcode or gcode.startswith(";"):  # Ignore empty lines and comments
                continue
            print(f"Sending: {gcode}")  
            ser.write((gcode + "\n").encode())  # Send command
            time.sleep(0.05)  # Small delay

            # Wait for Arduino response (optional)
            while (True):
                response = ser.readline().decode().strip()
                print(response)
                print(response == "COMPLETE")
                if (response == "COMPLETE"):
                    break
                # if response:
                    # print(f"Arduino: {response}")


if __name__ == '__main__':
    file_path = sys.argv[1]

# Path to your GCode file
    # GCODE_FILE = "output\heuristic_konan.gcode"

# Send the GCode file
    send_gcode(file_path)

# Close serial connection
    ser.close()
    print("Done.")
