import pyglet
from pyglet.window import key

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

player = pyglet.media.Player()
player.loop = True
player2 = pyglet.media.Player()


@window.event
def on_draw():
    window.clear()
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print(f'The key {symbol} was pressed')
    if symbol == key.A:
        print('The "A" key was pressed.')
        music = pyglet.media.synthesis.Sine(3.0, frequency=440, sample_rate=44800)
        player.queue(music)
        player.play()
    if symbol == key.B:
        print('The "B" key was pressed.')
        music = pyglet.media.synthesis.Sine(3.0, frequency=880, sample_rate=44800)
        player2.queue(music)
        player2.play()

@window.event
def on_key_release(symbol, modifiers):
    print("Stop")
    if symbol == key.A:
        player.pause()

pyglet.app.run()