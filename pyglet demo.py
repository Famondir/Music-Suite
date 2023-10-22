import pyglet
from pyglet.window import key

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

# player = pyglet.media.Player()
# player2 = pyglet.media.Player()
playerlist = []

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
    120: 62, 51: 62
    }

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

@window.event
def on_draw():
    window.clear()
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(f'The key {symbol} was pressed')
    if symbol in keymapping:
        player = TonePlayer(keymapping[symbol])
        playerlist.append(player)
        player.playTone()
"""     if symbol == key.A:
        print('The "A" key was pressed.')
        music = pyglet.media.load("wav/Accordion 058.wav", streaming=False)
        player.queue(music)
        player.play()
    if symbol == key.B:
        print('The "B" key was pressed.')
        music = pyglet.media.load("wav/Accordion 076.wav", streaming=False)
        # music = pyglet.media.synthesis.Sine(3.0, frequency=440, sample_rate=44800)
        player2.queue(music)
        player2.play() """

@window.event
def on_key_release(symbol, modifiers):
    print(f'The key {symbol} was released')
    if symbol in keymapping:
        for player in playerlist:
            if keymapping[symbol] == player.getmidiTone():
                player.stopTone()
                del player
"""     if symbol == key.A:
        print("Stop")
        player.pause()
    if symbol == key.B:
        print("Stop")
        player2.pause() """
        

pyglet.app.run()