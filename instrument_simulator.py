import pyglet
import accordion

# creating a window for the GUI
window = pyglet.window.Window(960, 540)
# setting the background color to white
pyglet.gl.glClearColor(1,1,1,1)

# creates a container for graphical elements for simple draw statement
accordion_batch = pyglet.graphics.Batch()
buttonBoard = accordion.ButtonBoard(0,300,window.width,200,accordion_batch)
keymapping = accordion.keymapping
playerlist = []

@window.event
def on_draw():
    window.clear()
    accordion_batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(f'The key {symbol} was pressed')
    if symbol in keymapping:
        # adds an audio player corresponding to the pressed key
        player = accordion.TonePlayer(keymapping[symbol])
        playerlist.append(player)
        player.play_tone()
        # highlights button corresponding to the pressed key
        buttonBoard.press_button(accordion.keymapping[symbol])

@window.event
def on_key_release(symbol, modifiers):
    print(f'The key {symbol} was released')
    if symbol in keymapping:
        # removes the audio player corresponding to the released key
        for player in playerlist:
            if keymapping[symbol] == player.get_midi_tone():
                player.stop_tone()
                del player
        # removes highlighting of button corresponding to the released key
        buttonBoard.release_button(keymapping[symbol])

pyglet.app.run()