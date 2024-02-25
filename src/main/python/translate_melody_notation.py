import functools, operator
import pandas as pd
from os.path import exists


class InvalidFileStructureException(Exception):
    def __init__(self, message="Can't identify unique setting block wrapped in \{\}."):
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

split_by_signs = lambda string, signs: tuple(
    string for string in string.split(signs) if string != ""
    )
seperate_settings_and_melody_part = functools.partial(split_by_signs, signs = "}")
split_by_measure = functools.partial(split_by_signs, signs = "|")
split_by_tone = functools.partial(split_by_signs, signs = ")")
split_tone_group = functools.partial(split_by_signs, signs = ",")
remove_opening_parenthesis = lambda iterable: tuple(map(lambda string: string.strip("("), iterable))

def get_tone_by_midi_nr(number, midi_to_tones_df):
    return midi_to_tones_df[midi_to_tones_df["midi"] == int(number)].iloc[0]["tone"]

def convert_midi_to_tone(iterable):
    midi_to_tones_df = pd.read_csv("./src/main/data/MIDI_to_tones_long.csv")
    splitted_tones = tuple(map(split_tone_group, iterable))
    return tuple(map(
        lambda tpl: tuple([get_tone_by_midi_nr(entry, midi_to_tones_df) if idx == 0
                     else entry for idx, entry in enumerate(tpl)]),
        splitted_tones)
    )

join_for_reduce = lambda a, b: a+","+b

def translate_melody_midi2tone(file_path, new_file_path):
    with open(file_path) as sheetmusic:
        data = sheetmusic.read().replace("\n", "")
        settings_string, melody_string = check_file_structure(
            seperate_settings_and_melody_part(data)
        )
        # print(settings_string)

        measure_tuple = split_by_measure(melody_string)
        # print(measure_tuple)

        tone_tuple = map(split_by_tone, measure_tuple)
        flattened_tone_tuple = functools.reduce(operator.concat, tone_tuple)
        clenaed_tone_tuple = remove_opening_parenthesis(flattened_tone_tuple)
        converted_tone_tuple = convert_midi_to_tone(clenaed_tone_tuple)
        converted_melody_string = functools.reduce(operator.concat, tuple(map(
            lambda iterable: "("+functools.reduce(join_for_reduce, iterable)+")", 
            converted_tone_tuple
        )))
        
        final_string = settings_string+"}\n"+converted_melody_string
        file_mode = "w" if exists(new_file_path) else "x"
        with open(new_file_path, file_mode) as new_file:
            new_file.write(final_string)

if __name__ == "__main__":
    translate_melody_midi2tone("./src/main/data/melodies/abend_ward.mdy", "./src/main/data/melodies/abend_ward.tdy")