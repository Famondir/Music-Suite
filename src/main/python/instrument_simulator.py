import pyglet
import accordion

# creating a window for the GUI
window_width = 960
window_height = 540
window = pyglet.window.Window(window_width, window_height)

# setting the background color to white
pyglet.gl.glClearColor(1, 1, 1, 1)

# creates a container for graphical elements for simple draw statement
accordion_batch = pyglet.graphics.Batch()

# gets a reference to the accordion board element
# side effect: it attaches all shapes to the accordion_batch
x_pos = 0
y_pos = 300
button_board_width = window.width
button_board_height = 200
buttonBoard = accordion.ButtonBoard(
    x_pos, y_pos, button_board_width, button_board_height, accordion_batch
)

keymapping = accordion.keymapping
players = []


@window.event
def on_draw():
    window.clear()
    accordion_batch.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol in keymapping:
        print(f'The key {symbol} was pressed -> MIDI tone {keymapping[symbol]}.')
        # adds an audio player corresponding to the pressed key
        player = accordion.TonePlayer(keymapping[symbol])
        players.append(player)
        player.play_tone()
        # highlights button corresponding to the pressed key
        buttonBoard.press_button(accordion.keymapping[symbol])
    else:
        print("This key is not supported.")


@window.event
def on_key_release(symbol, modifiers):
    print(f'The key {symbol} was released')
    if symbol in keymapping:
        # removes the audio player corresponding to the released key
        for player in players:
            if keymapping[symbol] == player.get_midi_tone():
                player.stop_tone()
                del player
        # removes highlighting of button corresponding to the released key
        buttonBoard.release_button(keymapping[symbol])


if __name__ == "__main__":
    pyglet.app.run()
