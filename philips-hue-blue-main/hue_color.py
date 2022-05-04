import sys
from bleak import BleakClient
from bleak import BleakScanner
import asyncio



def convert_rgb(rgb):
    scale = 0xFF
    adjusted = [max(1, chan) for chan in rgb]
    total = sum(adjusted)
    adjusted = [int(round(chan / total * scale)) for chan in adjusted]

    # Unknown, Red, Blue, Green
    return bytearray([0x1, adjusted[0], adjusted[2], adjusted[1]])

async def hue(colorin):
    ADDRESS = "D8:BD:5B:28:25:A6"
    #ADDRESS = "31:2e:38:38:2e:32"
    for x in range(0, len(colorin)):
        colorin[x] = int(colorin[x])
    LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
    BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
    TEMPERATURE_CHARACTERISTIC = "932c32bd-0004-47a2-835a-a8d455b859dd"
    COLOR_CHARACTERISTIC = "932c32bd-0005-47a2-835a-a8d455b859dd"
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        paired = await client.pair(protection_level=2)
        print("Paired")
        color = convert_rgb(colorin)
        await client.write_gatt_char(COLOR_CHARACTERISTIC, color)
        await asyncio.sleep(1.0)

asyncio.run(hue([sys.argv[1],sys.argv[2],sys.argv[3]]))
