#!/usr/bin/env python3
"""
LRI AEM-60DC8 — Modbus RTU Slave Simulator
=============================================

Emulates the holding-register map of the real LRI-AEM-60DC8 industrial DC
monitor so SCADA / HMI / PLC integrators can develop and test against a
realistic Modbus RTU server without the physical hardware on the bench.

Mirrors firmware v1.03:
  • 8 analog DC voltage channels at HR 40001..40008 (uint16, ×100, V)
  • NTC temperature at HR 40009 (int16, ×100, °C)
  • NTC min / max thresholds at HR 40010..40011 (R/W)
  • Per-channel min / max thresholds at HR 40012..40027 (R/W)
  • Baudrate index at HR 40028 (R/W, 0=4800 .. 4=115200)
  • Slave address at HR 40029 (R)
  • Function codes 03 (read holding) and 16 (write multiple)
  • Exception 02 on invalid address

The voltages drift around realistic nominal values with small noise so the
output mimics a real installation. Edit `CHANNELS` to model a different
deployment (telecom 48 V, automotive 12/24, solar 150 V, etc.).

Usage
-----
  pip install pymodbus pyserial
  python aem_60dc8_slave.py --port /dev/ttyUSB0 --slave-id 1 --baud 19200

On Windows:
  python aem_60dc8_slave.py --port COM3 --slave-id 1 --baud 19200

Or run over TCP for development without a serial port:
  python aem_60dc8_slave.py --tcp 0.0.0.0:5020

Quick test from another machine with pymodbus client:
  from pymodbus.client import ModbusTcpClient
  c = ModbusTcpClient("127.0.0.1", port=5020)
  c.connect()
  r = c.read_holding_registers(0, count=8, slave=1)
  print([v / 100.0 for v in r.registers])

License: MIT (provided as-is by LRI Automação Industrial for integration tests).
"""
from __future__ import annotations

import argparse
import logging
import random
import threading
import time
from dataclasses import dataclass

# Compatibility imports — pymodbus 3.x vs 2.x.
try:
    from pymodbus.datastore import (
        ModbusSequentialDataBlock,
        ModbusServerContext,
        ModbusSlaveContext,
    )
    from pymodbus.server import StartSerialServer, StartTcpServer
except ImportError as exc:
    raise SystemExit(
        "pymodbus is required:  pip install pymodbus pyserial"
    ) from exc

BAUDRATES = [4800, 9600, 19200, 38400, 57600, 115200]


@dataclass
class Channel:
    label: str
    nominal: float
    swing: float
    min_thr: float
    max_thr: float


# Default profile: mixed 48 V battery bank + 24 V aux + 12 V telecom + rectifier
CHANNELS: list[Channel] = [
    Channel("BAT CELL A", 53.6, 0.18, 48.0, 57.6),
    Channel("BAT CELL B", 53.7, 0.18, 48.0, 57.6),
    Channel("BAT CELL C", 53.5, 0.20, 48.0, 57.6),
    Channel("BAT CELL D", 53.6, 0.20, 48.0, 57.6),
    Channel("AUX BUS 24V", 24.1, 0.12, 22.5, 28.5),
    Channel("AUX BUS 24V", 24.1, 0.12, 22.5, 28.5),
    Channel("TELECOM 12V", 12.5, 0.08, 11.0, 14.4),
    Channel("RECT OUT", 27.4, 0.14, 24.0, 30.0),
]


class AemContext:
    """Wraps the pymodbus slave context and updates voltages on a tick."""

    def __init__(self, slave_id: int, baud_index: int) -> None:
        self.slave_id = slave_id
        self.baud_index = baud_index
        self.voltages = [c.nominal for c in CHANNELS]
        self.ntc_temperature = 23.6

        block = ModbusSequentialDataBlock(0, [0] * 32)
        self.slave = ModbusSlaveContext(hr=block)
        self.context = ModbusServerContext(slaves={slave_id: self.slave}, single=False)
        self._refresh_registers()

    def _refresh_registers(self) -> None:
        regs: list[int] = []
        for v in self.voltages:
            regs.append(int(round(v * 100)))
        regs.append(int(round(self.ntc_temperature * 100)) & 0xFFFF)
        # thresholds default; pymodbus block has 32 slots — fill the rest.
        regs.append(int(round(-10 * 100)) & 0xFFFF)  # NTC min
        regs.append(int(round(65 * 100)) & 0xFFFF)   # NTC max
        for c in CHANNELS:
            regs.append(int(round(c.min_thr * 100)))
            regs.append(int(round(c.max_thr * 100)))
        regs.append(self.baud_index)
        regs.append(self.slave_id)
        self.slave.setValues(3, 0, regs)

    def tick(self) -> None:
        """Drift voltages around their nominal values with small Gaussian noise."""
        for i, ch in enumerate(CHANNELS):
            drift = (ch.nominal - self.voltages[i]) * 0.12
            noise = (random.random() - 0.5) * ch.swing
            self.voltages[i] = round(self.voltages[i] + drift + noise, 2)
        self.ntc_temperature = round(
            self.ntc_temperature + (24.0 - self.ntc_temperature) * 0.1
            + (random.random() - 0.5) * 0.4,
            2,
        )
        self._refresh_registers()


def run_ticker(ctx: AemContext, interval: float = 1.0) -> None:
    while True:
        ctx.tick()
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("Usage")[0].strip())
    parser.add_argument("--slave-id", type=int, default=1, help="Modbus slave address (1-247)")
    parser.add_argument("--baud-index", type=int, default=2, help="0=4800 1=9600 2=19200 3=57600 4=115200")
    parser.add_argument("--port", type=str, help="Serial port for RTU mode (e.g. /dev/ttyUSB0 or COM3)")
    parser.add_argument("--tcp", type=str, help="host:port for TCP mode (e.g. 0.0.0.0:5020)")
    parser.add_argument("--baud", type=int, default=19200, help="Baudrate for serial mode")
    parser.add_argument("--tick", type=float, default=1.0, help="Voltage update interval in seconds")
    args = parser.parse_args()

    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    log = logging.getLogger("aem-sim")

    ctx = AemContext(slave_id=args.slave_id, baud_index=args.baud_index)
    ticker = threading.Thread(target=run_ticker, args=(ctx, args.tick), daemon=True)
    ticker.start()

    log.info(f"AEM-60DC8 simulator — slave_id={args.slave_id}, baud={BAUDRATES[args.baud_index]}")
    log.info("Holding registers: 40001..40008 voltages, 40009 NTC, 40028 baud idx, 40029 slave id")

    if args.tcp:
        host, port_str = args.tcp.split(":")
        log.info(f"Listening on TCP {host}:{port_str}")
        StartTcpServer(context=ctx.context, address=(host, int(port_str)))
    elif args.port:
        log.info(f"Serving RTU on {args.port} @ {args.baud}")
        StartSerialServer(
            context=ctx.context,
            port=args.port,
            baudrate=args.baud,
            stopbits=1,
            bytesize=8,
            parity="N",
            framer="rtu",
        )
    else:
        parser.error("Provide either --port for RTU or --tcp host:port for TCP mode")


if __name__ == "__main__":
    main()
