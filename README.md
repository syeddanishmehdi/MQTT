# Cumulocity IoT 3D Printer Simulator

A Python MQTT client that simulates a 3D printer device in Cumulocity IoT using SmartREST templates.

---

## Features

- Device registration and heartbeat  
- Simulated measurements (temperature, vibration, voltage, etc.)  
- Alarm and event generation  
- Remote restart capability  
- SmartREST template implementation  
- Thread-safe MQTT operations  

---

## Prerequisites

- Python 3.8+
- Cumulocity IoT tenant
- Paho MQTT client:


---

## Configuration

1. Replace placeholders in `mqttsensor.py`:

  ```
  SERVER_URL = "your-tenant.cumulocity.com"
  CLIENT_ID = "your-device-id"
  DEVICE_NAME = "Your Device Name"
  TENANT = "your-tenant-id"
  USERNAME = "your-username"
  PASSWORD = "your-password"
  ```

2. (Optional) Modify measurement ranges and intervals in the code as needed.

---

## Device Operations in Cumulocity

- **View measurements**: Navigate to Device → Measurements
- **Trigger restart**: Send `510` command to device control channel
- **Monitor alarms**: Check Device → Alarms

---

## Security Note

- This example uses basic authentication. For production:
  - Use certificate-based authentication
  - Store credentials securely (e.g., environment variables)
  - Enable TLS encryption






