import pyglet
from .. import scene_manager


class Menu(scene_manager.Scene):
    def __init__(self, window):
        super(Menu, self).__init__(window)
        self.i = 0
        self.j = 0
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.labels = {}
        self.items = ['PLAY', 'INSTRUCTIONS', 'OPTIONS', 'QUIT']
        self.select_item = 0
        for i in range(len(self.items)):
            self.labels[self.items[i]] = pyglet.text.Label('{}'.format(self.items[i]), font_name='Yonezawa',
                                                           font_size=25, color=(0, 255, 0, 0),
                                                           x=self.window.width // 2,
                                                           y=self.window.height // 7 * (4 - i),
                                                           anchor_x='center',
                                                           anchor_y='center',
                                                           batch=self.batch)

        self.title = pyglet.text.Label('CRYPTOGRAM',
                                       font_name='Yonezawa',
                                       font_size=40,
                                       x=self.window.width // 2, y=self.window.height // 2,
                                       anchor_x='center', anchor_y='center')

        self.soundtrack = pyglet.resource.media('screen.wav')
        self.soundtrack.play()

        @self.window.event
        def on_key_press(symbol, modifiers):
            soundtrack = pyglet.resource.media('choice.wav')
            soundtrack.play()
            if symbol == pyglet.window.key.UP:
                self.select_item = (self.select_item - 1) % len(self.items)
            elif symbol == pyglet.window.key.DOWN:
                self.select_item = (self.select_item + 1) % len(self.items)
            elif symbol == pyglet.window.key.ENTER:
                self.check_next()

    def check_next(self):
        if self.items[self.select_item] == 'PLAY':
            self.done = True
            self.next = 'LEVEL'
        elif self.items[self.select_item] == 'INSTRUCTIONS':
            self.done = True
            self.next = 'INSTR'
        elif self.items[self.select_item] == 'OPTIONS':
            self.done = True
            self.next = 'OPTION'
        elif self.items[self.select_item] == 'QUIT':
            pyglet.app.exit()

    def draw_background(self):
        if self.i < 255:
            self.i += 5
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                             0, 0, self.window.width, 0, self.window.width, self.window.height, 0, self.window.height)),
                             ('c3B', (127, 255, 0, 255, 255, 0, 255, 127, 0, self.i, self.i, self.i)))

    def draw_text(self, dt):
        self.title.color = (0, 0, 255, self.i)
        title_pos = self.window.height // 6 * 5
        if self.title.y <= title_pos:
            self.title.y += 5
        self.title.draw()
        if self.title.y >= title_pos:
            self.j += 2
            for i in self.labels:
                self.labels[i].color = (0, 255, 0, min(self.j * self.labels[i].y // 100, 255))

            self.labels[self.items[self.select_item]].color = (0, 0, 255, 255)
            self.batch.draw()

    def update(self, dt):
        self.window.clear()
        self.draw_background()
        self.draw_text(dt)
