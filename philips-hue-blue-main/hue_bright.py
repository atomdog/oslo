import sys
from bleak import BleakClient
from bleak import BleakScanner
import asyncio

async def bright(valin):
    valin = int(valin)
    ADDRESS = "D8:BD:5B:28:25:A6"
    #ADDRESS = "31:2e:38:38:2e:32"
    LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
    BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
    TEMPERATURE_CHARACTERISTIC = "932c32bd-0004-47a2-835a-a8d455b859dd"
    COLOR_CHARACTERISTIC = "932c32bd-0005-47a2-835a-a8d455b859dd"
    async with BleakClient(ADDRESS) as client:
        print("bright: "+ str(valin))
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")
        await client.write_gatt_char(
                    BRIGHTNESS_CHARACTERISTIC,
                    bytearray(
                        [
                            valin,
                        ]
                    ),
                )

asyncio.run(bright(sys.argv[1]))
