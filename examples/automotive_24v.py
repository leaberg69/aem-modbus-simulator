#!/usr/bin/env python3
"""
Preset: 24V automotive auxiliary systems scenario.

Models a fleet vehicle DC monitoring deployment: 4 chassis batteries (24V
nominal) plus 4 auxiliary circuits, useful for fleet telemetry.

Usage:
    python examples/automotive_24v.py --tcp 0.0.0.0:5020
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aem_60dc8_slave import Channel, main as run_simulator
import aem_60dc8_slave

aem_60dc8_slave.CHANNELS = [
    Channel("BAT-1 24V", 26.8, 0.4, 22.0, 28.5),
    Channel("BAT-2 24V", 26.9, 0.4, 22.0, 28.5),
    Channel("BAT-3 24V", 26.7, 0.4, 22.0, 28.5),
    Channel("BAT-4 24V", 27.0, 0.4, 22.0, 28.5),
    Channel("AUX-1 24V", 24.5, 0.3, 20.0, 28.0),
    Channel("AUX-2 24V", 24.6, 0.3, 20.0, 28.0),
    Channel("AUX-3 24V", 24.4, 0.3, 20.0, 28.0),
    Channel("AUX-4 24V", 24.7, 0.3, 20.0, 28.0),
]

if __name__ == "__main__":
    run_simulator()
