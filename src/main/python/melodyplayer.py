from accordion import TonePlayer
from threading import Timer
import asyncio


class InvalidAccordLengthException(Exception):
    def __init__(self, message="There is more than one accord listed."):
        self.message = message
        super().__init__(self.message)


def end_tone(player):
    player.stop_tone()
    del player


async def play_tone_aio(tone_nr, duration):
    player = TonePlayer(tone_nr)
    # playerlist.append(player)
    player.play_tone()
    await asyncio.sleep(duration)
    end_tone(player)


def play_tone_parallel(tone_nr, duration):
    for player in playerlist:
        end_tone(player)

    player = TonePlayer(tone_nr)
    playerlist.append(player)
    player.play_tone()
    t = Timer(duration, end_tone, [player])
    t.start()


def play_accord(accord, measure_duration):
    match accord:
        case "C":
            play_tone_parallel(60, measure_duration)
            play_tone_parallel(64, measure_duration)
            play_tone_parallel(67, measure_duration)
        case "F":
            play_tone_parallel(60, measure_duration)
            play_tone_parallel(65, measure_duration)
            play_tone_parallel(69, measure_duration)
        case "G":
            play_tone_parallel(71, measure_duration)
            play_tone_parallel(62, measure_duration)
            play_tone_parallel(67, measure_duration)
        case _:
            pass


def get_settings(data):
    settings_list = data.split("}")[0].strip("{").split(",")
    settings = {"bpm": 60, "beat_measure": 4}  # default values

    for entry in settings_list:
        option, value = entry.split(":")
        try:
            settings[option] = int(value)
        except ValueError:
            settings[option] = value

    return settings


async def main():
    with open("./src/main/data/melodies/abend_ward.mdy") as sheetmusic:
        data = sheetmusic.read().replace("\n", "")
        transpose = 12
        last_accord = None

        settings = get_settings(data)
        # print(settings)

        measure_duration = 60 / settings["bpm"] * settings["beat_measure"]  # in seconds
        # print(measure_duration)

        melody_list = \
            [tone.replace("(", "") for tone in data.split("}")[1].split(")")]
        # print(melody_list)

        for tone in melody_list[:-1]:
            midi_nr, denumerator, *accord = tone.split(",")

            if "|" in midi_nr:
                midi_nr = midi_nr.strip("|")
                if len(accord) == 0:
                    play_accord(last_accord[0], measure_duration)

            if len(accord) == 1:
                # print(accord)
                last_accord = accord
                play_accord(accord[0], measure_duration)
            elif len(accord) > 1:
                raise InvalidAccordLengthException()

            fraction = 1.5 / int(denumerator.strip(".")) \
                if "." in denumerator \
                else 1 / int(denumerator)
            duration = measure_duration * fraction

            await play_tone_aio(int(midi_nr) + transpose, duration)


if __name__ == "__main__":
    playerlist = []
    asyncio.run(main())
