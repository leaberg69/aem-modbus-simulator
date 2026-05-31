#!/usr/bin/env python3
"""
Preset: 8 PV solar string monitoring scenario.

Models 8 strings of solar PV panels with realistic open-circuit voltages
in the 30-45V range with weather-dependent variation (+/-2V swing).

Usage:
    python examples/solar_strings.py --tcp 0.0.0.0:5020
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aem_60dc8_slave import Channel, main as run_simulator
import aem_60dc8_slave

aem_60dc8_slave.CHANNELS = [
    Channel("STR-1 PV",  42.0, 2.0, 30.0, 50.0),
    Channel("STR-2 PV",  41.8, 2.0, 30.0, 50.0),
    Channel("STR-3 PV",  42.2, 2.0, 30.0, 50.0),
    Channel("STR-4 PV",  41.9, 2.0, 30.0, 50.0),
    Channel("STR-5 PV",  42.1, 2.0, 30.0, 50.0),
    Channel("STR-6 PV",  41.7, 2.0, 30.0, 50.0),
    Channel("STR-7 PV",  42.0, 2.0, 30.0, 50.0),
    Channel("STR-8 PV",  41.6, 2.0, 30.0, 50.0),
]

if __name__ == "__main__":
    run_simulator()
