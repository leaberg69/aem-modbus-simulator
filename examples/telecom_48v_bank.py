#!/usr/bin/env python3
"""
Preset: 8-cell 48V telecom battery bank monitoring scenario.

Models a typical telecom site DC plant: 8 string cells at ~53.6V nominal each,
NTC sensor for cabinet temperature, with realistic +/-0.18V noise drift.

Usage:
    python examples/telecom_48v_bank.py --tcp 0.0.0.0:5020
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aem_60dc8_slave import Channel, main as run_simulator

# Override the default profile with telecom 48V preset
import aem_60dc8_slave
aem_60dc8_slave.CHANNELS = [
    Channel("CELL-A1 48V", 53.6, 0.18, 48.0, 57.6),
    Channel("CELL-A2 48V", 53.7, 0.18, 48.0, 57.6),
    Channel("CELL-A3 48V", 53.5, 0.18, 48.0, 57.6),
    Channel("CELL-A4 48V", 53.8, 0.18, 48.0, 57.6),
    Channel("CELL-B1 48V", 53.6, 0.18, 48.0, 57.6),
    Channel("CELL-B2 48V", 53.7, 0.18, 48.0, 57.6),
    Channel("CELL-B3 48V", 53.4, 0.18, 48.0, 57.6),
    Channel("CELL-B4 48V", 53.9, 0.18, 48.0, 57.6),
]

if __name__ == "__main__":
    run_simulator()
