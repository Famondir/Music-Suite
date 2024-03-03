import functools
import operator
import pandas as pd
from os.path import exists
from functional import seq


class InvalidFileStructureException(Exception):
    def __init__(self, message="Can't identify unique setting block wrapped in {}."):
        self.message = message
        super().__init__(self.message)


# this function has a side effect described in its name
def seperate_settings_and_melody_part_and_check_file_structure(string):
    parts = tuple(string.split("}"))
    return check_file_structure(parts)


# this is the side effect: potentially raising an error
def check_file_structure(tuple_of_strings):
    if len(tuple_of_strings) != 2:
        raise InvalidFileStructureException()
    else:
        return tuple_of_strings


def split_by_signs_factory(signs):
    return lambda string: tuple(
        string for string in string.split(signs) if string != ""
    )


seperate_settings_and_melody_part2 = split_by_signs_factory("}")


split_by_signs = lambda string, signs: tuple(
    string for string in string.split(signs) if string != ""
)
seperate_settings_and_melody_part = functools.partial(split_by_signs, signs="}")
split_by_measure = functools.partial(split_by_signs, signs="|")
split_by_tone = functools.partial(split_by_signs, signs=")")
split_tone_group = functools.partial(split_by_signs, signs=",")
remove_opening_parenthesis = lambda string: string.strip("(")
join_for_reduce = lambda a, b: a + "," + b


def get_tone_by_midi_nr(number, midi_to_tones_df):
    return midi_to_tones_df[midi_to_tones_df["midi"] == int(number)].iloc[0]["tone"]


def convert_midi_to_tone(iterable):
    midi_to_tones_df = pd.read_csv("./src/main/data/MIDI_to_tones_long.csv")
    # print(iterable)
    splitted_tones = tuple(split_tone_group(iterable))
    # print(splitted_tones)
    return tuple(
        [
            get_tone_by_midi_nr(entry, midi_to_tones_df)
            if idx == 0
            else entry
            for idx, entry in enumerate(splitted_tones)
        ]
    )


def translate_melody_midi2tone(file_path, new_file_path):
    with open(file_path) as sheetmusic:
        data = sheetmusic.read().replace("\n", "")
        settings_string, melody_string = check_file_structure(
            seperate_settings_and_melody_part(data)
        )
        # print(settings_string)

        measure_tuple = seq(split_by_measure(melody_string))\
            .map(split_by_tone)\
            .reduce(operator.concat)\
            .map(remove_opening_parenthesis)\
            .map(convert_midi_to_tone)\
            .map(lambda iterable: "(" + functools.reduce(join_for_reduce, iterable) + ")")\
            .reduce(operator.concat)

        # print(measure_tuple)

        final_string = settings_string + "}\n" + measure_tuple
        file_mode = "w" if exists(new_file_path) else "x"
        with open(new_file_path, file_mode) as new_file:
            new_file.write(final_string)


if __name__ == "__main__":
    translate_melody_midi2tone("./src/main/data/melodies/abend_ward.mdy", "./src/main/data/melodies/abend_ward.tdy")
