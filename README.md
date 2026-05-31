# AEM-60DC8 Modbus RTU/TCP Slave Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![pymodbus](https://img.shields.io/badge/pymodbus-3.x%20%7C%202.x-brightgreen)](https://github.com/pymodbus-dev/pymodbus)
[![Modbus](https://img.shields.io/badge/protocol-Modbus%20RTU%20%2F%20TCP-orange)](https://modbus.org/)
[![Firmware](https://img.shields.io/badge/mirrors-AEM--60DC8%20v1.03-blue)](https://aem.lri.com.br/en-us/firmware)

> Open-source Python simulator that emulates the full holding-register map of the **[LRI AEM-60DC8](https://aem.lri.com.br/en-us)** industrial DC voltage monitor.

Lets SCADA / HMI / PLC integrators develop and test their Modbus integration **without the physical hardware on the bench** — useful for offline development, CI pipelines, and training environments.

## What it simulates

- **8 independent DC voltage channels** (0-60V, ±1% accuracy emulation)
- **NTC temperature sensor** with realistic drift
- **147 holding registers in 17 functional blocks** (full map at <https://aem.lri.com.br/en-us/modbus>)
- **Six baudrates**: 4800 / 9600 / 19200 / 38400 / 57600 / 115200
- **Function codes** 03 (Read Holding) and 16 (Write Multiple)
- **Exception 02** on invalid address
- **Configurable presets** for telecom 48V, solar strings, automotive 24V scenarios

## Quick start

### Install

```bash
pip install pymodbus pyserial
```

### Run as Modbus TCP server (no hardware needed)

```bash
python aem_60dc8_slave.py --tcp 0.0.0.0:5020 --slave-id 1
```

### Run as Modbus RTU over USB-RS485

```bash
# Linux / macOS
python aem_60dc8_slave.py --port /dev/ttyUSB0 --baud 19200 --slave-id 1

# Windows
python aem_60dc8_slave.py --port COM3 --baud 19200 --slave-id 1
```

### Test from any Modbus client

```python
from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient("127.0.0.1", port=5020)
c.connect()

# Read 8 DC channels (V, scaled ×100)
r = c.read_holding_registers(0, count=8, slave=1)
voltages = [v / 100.0 for v in r.registers]
print(f"Channels (V): {voltages}")

# Read NTC temperature (°C, scaled ×100)
t = c.read_holding_registers(8, count=1, slave=1)
print(f"Temperature (°C): {t.registers[0] / 100.0}")
```

## Register map (excerpt)

| Address     | Name                       | Type   | Scale | Unit | R/W |
| ----------- | -------------------------- | ------ | ----- | ---- | --- |
| 40001-40008 | Voltage CH1..CH8           | uint16 | ×100  | V    | R   |
| 40009       | NTC Temperature            | int16  | ×100  | °C   | R   |
| 40010-40011 | NTC min / max threshold    | int16  | ×100  | °C   | R/W |
| 40012-40027 | Per-channel min/max thresh | uint16 | ×100  | V    | R/W |
| 40028       | Baudrate index (0-5)       | uint16 | —     | —    | R/W |
| 40029       | Slave address              | uint16 | —     | —    | R   |

**Full 147-register map** with all 17 functional blocks (alarms, telemetry, anti-rollback counters, RTOS health, etc) is documented and interactively browsable at:

**<https://aem.lri.com.br/en-us/modbus>**

## Use cases

- **SCADA integration testing** (Ignition, Elipse E3, AVEVA InTouch, WinCC, etc.)
- **PLC program development** without physical hardware
- **CI/CD pipelines** for industrial automation projects
- **Engineering training** and educational labs
- **Pre-deployment validation** before site commissioning

## Customization

Edit the `CHANNELS` list in `aem_60dc8_slave.py` (or use the presets in `examples/`) to model your deployment scenario:

```python
CHANNELS: list[Channel] = [
    Channel("BAT CELL A", 53.6, 0.18, 48.0, 57.6),
    Channel("BAT CELL B", 53.7, 0.18, 48.0, 57.6),
    # ... 6 more channels
]
```

See `examples/` for ready-to-use presets:
- `telecom_48v_bank.py` — 8-cell 48V telecom battery bank
- `solar_strings.py` — 8 PV strings monitoring
- `automotive_24v.py` — 24V automotive auxiliary systems

## About the real hardware

The simulator emulates the [**LRI AEM-60DC8**](https://aem.lri.com.br/en-us), an industrial DC voltage monitoring platform with:

- 8 independent DC channels (0-60V, 30V and 150V variants)
- 5000 VAC rms galvanic isolation on opto-isolated digital inputs
- Modbus RTU over RS-485 (4,800-115,200 bps)
- Ed25519-signed firmware with 9-layer boot validation
- IEC 62443-4-2 Security Level 2 target
- 16×4 LCD with 3-key navigation
- 35 mm DIN rail mounting, UL94 V-0 flame retardant
- Manufactured in Brazil by [LRI Automação Industrial](https://lri.com.br)

For technical documentation, datasheet, and the interactive Modbus map:
**<https://aem.lri.com.br/en-us>**

## Contributing

Pull requests welcome! Common contributions:

- Additional preset scenarios in `examples/`
- Better simulation realism (drift patterns, noise models, fault injection)
- Additional Modbus function codes (currently 03 and 16)
- TCP/RTU bridging examples
- Test fixtures

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE).

This simulator is provided as-is by LRI Automação Industrial for the engineering community. The real AEM-60DC8 firmware and hardware are proprietary; only the Modbus map (which is a public interface anyway) is mirrored here.

## Links

- 🏭 [LRI Automação Industrial](https://lri.com.br) — Manufacturer
- 📋 [Full Modbus Map (interactive)](https://aem.lri.com.br/en-us/modbus)
- 📄 [AEM-60DC8 Datasheet (PDF)](https://aem.lri.com.br/datasheets/LRI-AEM-60DC8-datasheet-en.pdf)
- 📚 [Technical Whitepapers](https://aem.lri.com.br/en-us/whitepapers)
- 💼 [Compare vs other DC monitors](https://aem.lri.com.br/en-us/compare)
