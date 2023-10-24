import pyglet
from pyglet.window import key
from pyglet import shapes

window = pyglet.window.Window()
pyglet.gl.glClearColor(1,1,1,1)

keymapping = {
    944892805120: 53, 65505: 53, 
    65289: 54, 
    65509: 55, 
    60: 56, 
    49: 56, 
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
    46: 83, 48: 84,
    112: 85,
    824633720832: 86,
    45: 87, 940597837824: 87,
    798863917056: 88,
    953482739712: 89,
    65506: 90, 949187772416: 90,
    43: 91,
    35: 92,
    65288: 93
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
        self.startingTone = 60

        self.buttonList = []
        self.buttonList.append((Button(60, "c4", self.x+3*self.width/15, self.y-1*self.height/4, self.width/(2*15), 1, (0,0,0,255), (255,255,255,255), batch),))
        self.buttonList.append((Button(61, "c#4", self.x+3*self.width/15, self.y-2*self.height/4, self.width/(2*15), 1, (0,0,0,255), (0,0,0,255), batch),))
        self.buttonList.append((Button(62, "d4", self.x+3*self.width/15, self.y-3*self.height/4, self.width/(2*15), 1, (0,0,0,255), (255,255,255,255), batch),))
        self.buttonList.append((Button(63, "d#4", self.x+4*self.width/15, self.y-1*self.height/4, self.width/(2*15), 1, (0,0,0,255), (0,0,0,255), batch),))

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

    def getmidiTone(self):
        return self.midiTone    

batch = pyglet.graphics.Batch()
buttonBoard = ButtonBoard(100,300,400,200,batch)
playerlist = []

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(f'The key {symbol} was pressed')
    if symbol in keymapping:
        # player = TonePlayer(keymapping[symbol])
        # playerlist.append(player)
        # player.playTone()
        buttonBoard.pressButton(keymapping[symbol])

@window.event
def on_key_release(symbol, modifiers):
    print(f'The key {symbol} was released')
    if symbol in keymapping:
        buttonBoard.releaseButton(keymapping[symbol])
"""         for player in playerlist:
            if keymapping[symbol] == player.getmidiTone():
                player.stopTone()
                del player
 """        

pyglet.app.run()