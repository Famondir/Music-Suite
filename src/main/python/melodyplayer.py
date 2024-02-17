from accordion import TonePlayer
from threading import Timer
import asyncio

playerlist = []

def play_tone(tone_nr, duration):
    player = TonePlayer(tone_nr)
    playerlist.append(player)
    player.play_tone()
    t = Timer(duration, end_tone, [player])
    t.start()

def end_tone(player):
    player.stop_tone()
    del player

# play_tone(60, 3)
# play_tone(63, 3)
# play_tone(66, 3)

async def play_tone_aio(tone_nr, duration):
    player = TonePlayer(tone_nr)
    playerlist.append(player)
    player.play_tone()
    await asyncio.sleep(duration)
    end_tone(player)

async def main():
    await asyncio.gather(play_tone_aio(60,3), play_tone_aio(63,3), play_tone_aio(66,3))

asyncio.run(main())