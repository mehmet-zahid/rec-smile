import asyncio
import random

import edge_tts
from edge_tts import VoicesManager

TEXT = "Hoy es un buen día."
OUTPUT_FILE = "spanish.mp3"


async def _main() -> None:
    voices = await VoicesManager.create()
    voice = voices.find(Gender="Male", Language="es")
    # Also supports Locales
    # voice = voices.find(Gender="Female", Locale="es-AR")

    communicate = edge_tts.Communicate(TEXT, random.choice(voice)["Name"])
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(_main())