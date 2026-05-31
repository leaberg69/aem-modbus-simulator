# Changelog

## [1.0.0] — 2026-05-31

### Added
- Initial public release of the AEM-60DC8 Modbus RTU/TCP slave simulator
- Full mirror of firmware v1.03 holding register map (147 registers in 17 functional blocks)
- 8 independent DC voltage channels (0-60V, configurable nominal/swing/thresholds)
- NTC temperature sensor simulation
- Six baudrates: 4800 / 9600 / 19200 / 38400 / 57600 / 115200
- Realistic noise simulation around nominal values
- TCP mode (for development without serial hardware)
- Serial mode (for testing with real USB-RS485 adapters)
- Example presets: telecom 48V bank, solar strings, automotive 24V
- pymodbus 2.x and 3.x compatibility
- MIT License

### Documentation
- Full holding register map at <https://aem.lri.com.br/en-us/modbus>
- Reference implementation at <https://github.com/leaberg69/aem-modbus-simulator>
