"""Smoke tests for the register map structure."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aem_60dc8_slave import BAUDRATES, CHANNELS


def test_baudrates_complete():
    """All 6 standard baudrates must be supported (firmware v1.03)."""
    assert BAUDRATES == [4800, 9600, 19200, 38400, 57600, 115200]


def test_eight_channels():
    """AEM-60DC8 has exactly 8 DC voltage channels."""
    assert len(CHANNELS) == 8


def test_channel_thresholds_consistent():
    """Min threshold must be below nominal which must be below max."""
    for ch in CHANNELS:
        assert ch.min_thr <= ch.nominal <= ch.max_thr, f"Inconsistent: {ch}"
