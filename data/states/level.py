import os
import json
import pyglet
from .. import scene_manager



class LevelChoose(scene_manager.Scene):
    def __init__(self,window):
        super(LevelChoose,self).__init__(window)
        self.window = window
        self.i = 0
        self.batch = pyglet.graphics.Batch()
        self.label_dict = {}
        self.mark_level = 1
        p = os.path.join('resources', 'levels','complete_levels.json')
        with open(p,'r') as f:
            d = json.load(f)
        self.complete_level = d

        self.title = pyglet.text.Label('CRYPTOGRAM',
                               color=(0, 0, 255, 255),
                               font_name='Yonezawa',
                               font_size= 40,
                               x= self.window.width // 2, y =self.window.height // 6*5,
                               anchor_x='center', anchor_y='center', batch = self.batch)
        for i in range(18):
            self.label_dict[i+1] = pyglet.text.Label('LEVEL{}'.format(i+1),
                                                   color = (255,127,0,255//6*(i//3+1)),
                                                   font_name = 'Yonezawa',
                                                   font_size = 15,
                                                   x = self.window.width // 4 * (i%3+1),
                                                   y = self.window.height// 9 *(6-i//3),
                                                   anchor_x = 'center',
                                                   anchor_y = 'center',
                                                   batch = self.batch)


        @self.window.event
        def on_key_press(symbol,modifiers):
            soundtrack = pyglet.resource.media('choice.wav')
            soundtrack.play()
            if symbol == pyglet.window.key.RIGHT:
                self.mark_level = min(self.mark_level+1,18)

            elif symbol == pyglet.window.key.LEFT:
                self.mark_level = max(1,self.mark_level-1)

            elif symbol == pyglet.window.key.UP:
                self.mark_level = max((self.mark_level-1)%3+1,self.mark_level-3)

            elif symbol == pyglet.window.key.DOWN:
                self.mark_level = min(self.mark_level+3,(self.mark_level-1)%3+16)
            elif symbol in (pyglet.window.key.SPACE, pyglet.window.key.RETURN):
                self.persist = self.mark_level
                self.done = True
                self.next = 'GAME'
            elif symbol == pyglet.window.key.BACKSPACE:
                self.done = True
                self.next = 'MENU'

    def entry_actions(self, persist):
        self.mark_level = persist

    def draw_background(self):
        if self.i < 255:
            self.i += 5
            if self.i >= 255:
                self.i = 255
        a = self.i
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                             0, 0, self.window.width, 0, self.window.width, self.window.height, 0, self.window.height)),
                             ('c3B', (
                             127 + a // 2, 255, 0, 127 + a // 2, 255, 0, 255, 255, 255 ,255, 255, 255)))
    def draw_text(self):
        if len(self.complete_level)==18:
            self.title.text = 'ALL COMPLETE'
        self.title.draw()
        for i in range(18):
            self.label_dict[i + 1].color  = (255,127,0,255//6*(i//3+1))
        for i in self.complete_level:
            j = int(i)
            self.label_dict[j].color  = (0,255,0,255//6*((j-1)//3+1))
        self.label_dict[self.mark_level].color = (0,0,255,255)
        
        self.batch.draw()


    def update(self,dt):
        self.window.clear()
        self.draw_background()
        self.draw_text()




