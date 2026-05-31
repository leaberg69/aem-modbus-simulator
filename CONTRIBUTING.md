# Contributing to AEM-60DC8 Modbus Simulator

Thank you for your interest in contributing!

## Quick start

1. Fork the repo on GitHub
2. Create a feature branch: `git checkout -b my-feature`
3. Make your changes
4. Test locally: `python aem_60dc8_slave.py --tcp 0.0.0.0:5020`
5. Submit a pull request with a clear description

## Welcome contributions

### High value
- **Preset scenarios** in `examples/` (e.g., wind turbine DC bus, EV charging station, off-grid solar)
- **Realism improvements**: temperature-dependent drift, calendar aging models, fault injection
- **Test fixtures**: integration tests against real Ignition/Codesys/RAPID clients
- **Documentation**: deployment scenarios, integration guides

### Medium value
- **Modbus function code coverage** (currently 03 and 16, could add 01/02/04/05/06/15/17)
- **TCP/RTU gateway examples**
- **Performance benchmarks** vs real hardware

### Out of scope
- Replacing pymodbus with a different stack (compatibility matters)
- Adding GUI (this is a headless simulator for CI/testing)
- Vendor-specific extensions (this mirrors LRI AEM-60DC8 specifically)

## Code style

- Follow PEP 8
- Use type hints (Python 3.8+)
- Single-file design preferred for the main simulator
- Examples in `examples/` are self-contained

## Reporting issues

Found a discrepancy with the real AEM-60DC8 register map? Check the interactive map at <https://aem.lri.com.br/en-us/modbus> first, then file an issue with:

- Register address
- Expected value (per docs)
- Actual value (per simulator)
- Modbus client/SCADA being used

## License

By contributing, you agree your changes are released under the MIT license (same as the project).
