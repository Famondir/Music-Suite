import pyglet
from pyglet import shapes
from pyglet.window import key
import math

class BorderedCircle:
    def __init__(self, x, y, radius, borderwidth, color, fill, batch):
        self.circle = shapes.Circle(x=x, y=y, radius=radius, batch=batch)
        self.circle.color = color
        self.inner_circle = shapes.Circle(x=x, y=y, radius=radius-borderwidth, batch=batch)
        self.inner_circle.color = fill

    def change_fill(self, fill):
        self.inner_circle.color = fill


class Button:
    def __init__(self, tone, label, x, y, radius, borderwidth, color, fill, batch):
        self.fill = fill
        self.bordered_circle = BorderedCircle(x, y, radius, borderwidth, color, self.fill, batch)
        self.label = pyglet.text.Label(text=label,
                          font_name='Times New Roman',
                          font_size=12,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center', 
                          color=(255-fill[0],255-fill[1],255-fill[2],255),
                          batch=batch)
        self.tone = tone
        
    def press_button(self):
        self.bordered_circle.change_fill((240,170,70,255)) # kind of orange color

    def release_button(self):
        self.bordered_circle.change_fill(self.fill)


class ButtonBoard:
    def __init__(self, x, y, width, height, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.starting_tone = 53
        self.button_list = []

        scale = ["c","c#","d","d#","e","f","f#","g","g#","a","a#","h"]
        big_scale = []

        for i in range(3,7): # scale covers tones from octave 3 to 7
            for s in [s + str(i) for s in scale]:
                big_scale.append(s)
        big_scale = big_scale[5:-3] # but not all tones from 3rd and 7th octave

        for i in range(0,40):
            keys = list(keymapping.keys())
            values = list(keymapping.values())
            position = values.index(i+self.starting_tone) # get the position of the value that equals the tone
            key_symbol_string = key.symbol_string(keys[position])
            
            big_scale[i] = (i+self.starting_tone, big_scale[i], key_symbol_string)

        button_rows = math.ceil(len(big_scale)/3)
        radius = self.width/(2*button_rows+1)
        color = (0,0,0,255) # black
        borderwidth = 1
        x_offset = radius*5/3
        x_shift = self.width/button_rows
        y_shift = radius*2

        for el in big_scale:
            tone = el[0]
            label = f"{el[1]}"#\n{el[2]}"
            fill = (255,255,255,255)
            if "#" in label:
                fill = (0,0,0,255)

            if tone%3 == 2:
                button1 = Button(tone, label, self.x+x_offset+((tone-self.starting_tone)//3-1/3)*x_shift, self.y-3*y_shift, radius, borderwidth, color, fill, batch)
                button2 = Button(tone, label, self.x+x_offset+((tone-self.starting_tone)//3-1/3)*x_shift, self.y-0*y_shift, radius, borderwidth, color, fill, batch)
                self.button_list.append((button1, button2))
            elif tone%3 == 1:
                button1 = Button(tone, label, self.x+x_offset+((tone-self.starting_tone)//3+1/3)*x_shift, self.y-2*y_shift, radius, borderwidth, color, fill, batch)
                self.button_list.append((button1,))
            elif tone%3 == 0:
                button1 = Button(tone, label, self.x+x_offset+((tone-self.starting_tone)//3+0/3)*x_shift, self.y-1*y_shift, radius, borderwidth, color, fill, batch)
                self.button_list.append((button1,))

        self.button_list[-1] = (self.button_list[-1][1],)

    def press_button(self, tone):
        for button in self.button_list[tone-self.starting_tone]:
            button.press_button()

    def release_button(self, tone):
        for button in self.button_list[tone-self.starting_tone]:
            button.release_button()


class TonePlayer:
    def __init__(self, midi_tone):
        self.midi_tone = midi_tone
        self.player = pyglet.media.Player()
        self.music = pyglet.media.load("./src/main/data/wav/Accordion 0"+str(self.midi_tone)+".wav", streaming=False)

    def play_tone(self):
        self.player.queue(self.music)
        self.player.play()

    def stop_tone(self):
        self.player.pause()

    def get_midi_tone(self):
        return self.midi_tone
    

# maps the keys on a computer keyboard to the buttons on a button accordion
keymapping = {
    944892805120: 53, 94: 53, 65505: 53, 
    65289: 54, 
    65509: 55, 
    60: 56, 49: 56, 
    113: 57, 
    97: 58,     
    121: 59, 50: 59, 
    119: 60, 
    115: 61, 
    120: 62, 51: 62,
    101: 63,
    100: 64,
    99: 65, 52: 65,
    114: 66,
    102: 67,
    118: 68, 53: 68,
    116: 69,
    103: 70,
    98: 71, 54: 71,
    122: 72,
    104: 73,
    110: 74, 55: 74,
    117: 75,
    106: 76,
    109: 77, 56: 77,
    105: 78,
    107: 79,
    44: 80, 57: 80,
    111: 81,
    108: 82,
    46: 83, 48: 83,
    112: 84,
    824633720832: 85, 201863462912: 85,
    45: 86, 940597837824: 86, 85899345920: 86,
    798863917056: 87, 146028888064: 87,
    953482739712: 88, 206158430208: 88,
    949187772416: 89, 90194313216: 89, 65506: 89,
    43: 90,
    35: 91,
    65288: 92
}