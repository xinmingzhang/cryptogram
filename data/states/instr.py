import pyglet
from .. import scene_manager


class Instruction(scene_manager.Scene):
    def __init__(self, window):
        super(Instruction, self).__init__(window)
        self.window = window
        self.i = 0
        self.title = pyglet.text.Label('INSTRUCTIONS',
                                       font_name='Yonezawa',
                                       font_size=40,
                                       color=(0, 0, 255, 255),
                                       x=self.window.width // 2, y=self.window.height // 6 * 5,
                                       anchor_x='center', anchor_y='center')
        self.text_1 = '''<p> <font size = 5><font color = blue><font face = 'arial'>These puzzles have encoded by substituting one letter for another,your job is to decode them. Level 1 to 6 are from <em>The Confucian Analects</em>, level 7 to 12, <em>Dao De Jing</em>, level 13 to 18 ,<em>The Art of War</em>. These books are all classic in China culture, I copy the translations from <code>http://ctext.org/</code> you can get more if you are interested in.</font></font></font>'''
        self.text_2 = '''
                         <p><font size = 5><font color = blue><font face = 'arial'># Type the letters from keyboard</font></font></font>
                         <P><font size = 5><font color = blue><font face = 'arial'># LEFT,RIGHT: move the marker</font></font></font>
                         <P><font size = 5><font color = blue><font face = 'arial'># SPACE: get hint (only 3 times)</font></font></font>
                         <p><font size = 5><font color = blue><font face = 'arial'># BACKSPACE: get back</font></font></font>
                         <p><font size = 5><font color = blue><font face = 'arial'># Esc: quit</font></font></font>'''

        self.label = pyglet.text.HTMLLabel(self.text_1,
                                           width=self.window.width // 6 * 5, x=self.window.width // 2,
                                           y=self.window.height // 5 * 3,
                                           multiline=True, anchor_x='center', anchor_y='center')
        self.control_label = pyglet.text.HTMLLabel(self.text_2, width=self.window.width // 6 * 5, x= 180,
                                                   y=self.window.height // 5 * 2,
                                                   multiline=True, anchor_x='left', anchor_y='top')

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.BACKSPACE:
                self.done = True
                self.next = 'MENU'
            elif symbol == pyglet.window.key.ENTER:
                self.done = True
                self.next = 'LEVEL'

    def draw_background(self):
        if self.i < 255:
            self.i += 5
            if self.i >= 255:
                self.i = 255
        a = self.i
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                                 0, 0, self.window.width, 0, self.window.width, self.window.height, 0,
                                 self.window.height)),
                             ('c3B', (
                                 255 - a // 2, 255, 0, 255 - a // 2, 255, 0, 255, 255, 255, 255, 255, 255)))

    def draw_text(self):
        self.label.draw()
        self.title.draw()
        self.control_label.draw()

    def update(self,dt):
        self.window.clear()
        self.draw_background()
        self.draw_text()
