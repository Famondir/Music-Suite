class InvalidFileStructureException(Exception):
    def __init__(self, message="Can't identify unique setting block wrapped in \{\}."):
        self.message = message
        super().__init__(self.message)

def seperate_settings_and_melody_part_and_check_file_structure(string):
    parts = string.split("}")
    if len(parts) != 2:
        raise InvalidFileStructureException()
    else:
        return parts

def check_file_structure(list_of_strings):
    if len(list_of_strings) != 2:
        raise InvalidFileStructureException()
    else:
        return list_of_strings

seperate_settings_and_melody_part = lambda string: string.split("}")
split_by_measure = lambda string: string.split("|")
split_by_tone = lambda string: string.split(")")

def translate_melody_midi2tone(file_path):
    with open(file_path) as sheetmusic:
        data = sheetmusic.read().replace("\n", "")
        settings_string, melody_string = check_file_structure(
            seperate_settings_and_melody_part(data)
        )
        print(settings_string)

if __name__ == "__main__":
    translate_melody_midi2tone("./src/main/data/melodies/abend_ward.mdy")