import pyglet
from pyglet.window import key
from pyglet import shapes
import math

window = pyglet.window.Window(960, 540)
pyglet.gl.glClearColor(1,1,1,1)

keymapping = {
    944892805120: 53, 65505: 53, 
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
    824633720832: 85,
    45: 86, 940597837824: 86,
    798863917056: 87,
    953482739712: 88,
    65506: 89, 949187772416: 89,
    43: 90,
    35: 91,
    65288: 92
    }

class BorderedCircle:
    def __init__(self, x, y, radius, borderwidth, color, fill, batch):
        self.circle = shapes.Circle(x=x, y=y, radius=radius, batch=batch)
        self.circle.color = color
        self.innerCircle = shapes.Circle(x=x, y=y, radius=radius-borderwidth, batch=batch)
        self.innerCircle.color = fill

    def changeFill(self, fill):
        self.innerCircle.color = fill

class Button:
    def __init__(self, tone, label, x, y, radius, borderwidth, color, fill, batch):
        self.fill = fill
        self.borderedCircle = BorderedCircle(x, y, radius, borderwidth, color, self.fill, batch)
        self.label = pyglet.text.Label(text=label,
                          font_name='Times New Roman',
                          font_size=12,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center', 
                          color=(255-fill[0],255-fill[1],255-fill[2],255),
                          batch=batch)
        self.tone = tone
        
    def pressButton(self):
        self.borderedCircle.changeFill((255,180,90,255))

    def releaseButton(self):
        self.borderedCircle.changeFill(self.fill)

class ButtonBoard:
    def __init__(self, x, y, width, height, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.startingTone = 53
        self.buttonList = []

        scale = ["c","c#","d","d#","e","f","f#","g","g#","a","a#","h"]
        bigScale = []
        for i in range(3,7):
            for s in [s + str(i) for s in scale]:
                bigScale.append(s)
        bigScale = bigScale[5:-3]
        for i in range(0,40):
            bigScale[i] = (i+53, bigScale[i])

        buttonRows = math.ceil(len(bigScale)/3)
        radius = self.width/(2*buttonRows+1)
        color = (0,0,0,255) # black
        borderwidth = 1
        xOffset = radius*5/3
        xShift = self.width/buttonRows
        yShift = radius*2

        for el in bigScale:
            tone = el[0]
            label = el[1]
            fill = (255,255,255,255)
            if "#" in label:
                fill = (0,0,0,255)

            if tone%3 == 2:
                button1 = Button(tone, label, self.x+xOffset+((tone-53)//3+2/3)*xShift, self.y-3*yShift, radius, borderwidth, color, fill, batch)
                button2 = Button(tone, label, self.x+xOffset+((tone-53)//3-1/3)*xShift, self.y-0*yShift, radius, borderwidth, color, fill, batch)
                self.buttonList.append((button1, button2))
            elif tone%3 == 1:
                button1 = Button(tone, label, self.x+xOffset+((tone-53)//3+1/3)*xShift, self.y-2*yShift, radius, borderwidth, color, fill, batch)
                self.buttonList.append((button1,))
            elif tone%3 == 0:
                button1 = Button(tone, label, self.x+xOffset+((tone-53)//3+0/3)*xShift, self.y-1*yShift, radius, borderwidth, color, fill, batch)
                self.buttonList.append((button1,))

        self.buttonList[-1] = (self.buttonList[-1][1],)

    def pressButton(self, tone):
        for button in self.buttonList[tone-self.startingTone]:
            button.pressButton()

    def releaseButton(self, tone):
        for button in self.buttonList[tone-self.startingTone]:
            button.releaseButton()

class TonePlayer:
    def __init__(self, midiTone):
        self.midiTone = midiTone
        self.player = pyglet.media.Player()
        self.music = pyglet.media.load("wav/Accordion 0"+str(self.midiTone)+".wav", streaming=False)

    def playTone(self):
        self.player.queue(self.music)
        self.player.play()

    def stopTone(self):
        self.player.pause()

    def getMidiTone(self):
        return self.midiTone    

batch = pyglet.graphics.Batch()
buttonBoard = ButtonBoard(0,300,window.width,200,batch)
playerlist = []

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(f'The key {symbol} was pressed')
    if symbol in keymapping:
        player = TonePlayer(keymapping[symbol])
        playerlist.append(player)
        player.playTone()
        buttonBoard.pressButton(keymapping[symbol])

@window.event
def on_key_release(symbol, modifiers):
    print(f'The key {symbol} was released')
    if symbol in keymapping:
        for player in playerlist:
            if keymapping[symbol] == player.getMidiTone():
                player.stopTone()
                del player
        buttonBoard.releaseButton(keymapping[symbol])

pyglet.app.run()