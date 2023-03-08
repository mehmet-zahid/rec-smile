import asyncio
import json
import edge_tts
import subprocess


TEXT = "Merhaba. Sorununuz nedir efendim ?"
VOICE = "en-GB-SoniaNeural"
VOICE2 = "tr-TR-AhmetNeural"
OUTPUT_FILE = "test.mp3"



async def _main() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE2)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(_main())