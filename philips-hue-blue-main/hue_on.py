import sys
from bleak import BleakClient
from bleak import BleakScanner
import asyncio

async def light_on():
    ADDRESS = "D8:BD:5B:28:25:A6"
    #ADDRESS = "31:2e:38:38:2e:32"
    LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
    BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
    TEMPERATURE_CHARACTERISTIC = "932c32bd-0004-47a2-835a-a8d455b859dd"
    COLOR_CHARACTERISTIC = "932c32bd-0005-47a2-835a-a8d455b859dd"
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        paired = await client.pair(protection_level=2)
        print("Paired")
        await client.write_gatt_char(LIGHT_CHARACTERISTIC, b"\x01")
        await asyncio.sleep(1.0)

asyncio.run(light_on())
