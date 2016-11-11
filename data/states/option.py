import os
import json
import pyglet
import random
from .. import scene_manager



class Option(scene_manager.Scene):
    def __init__(self,window):
        super(Option,self).__init__(window)
        self.window = window
        self.i = 0
        self.fullscreen = False
        self.audio = True
        self.init = False
        self.shake = False        
        self.batch = pyglet.graphics.Batch()

        self.labels = {}
        self.items = ['FULLSCREEN', 'AUDIO', 'INITIALISE', 'SHAKE']

        self.title = pyglet.text.Label('OPTION',
                                       font_name='Yonezawa',
                                       font_size=40,
                                       color=(0, 255, 0, 255),
                                       x=self.window.width // 2, y=self.window.height // 6 * 5,
                                       anchor_x='center', anchor_y='center')

        self.select_item = 0
        for i in range(len(self.items)):
            self.labels[self.items[i]] = pyglet.text.Label('{}'.format(self.items[i]), font_name='Yonezawa',
                                                           font_size=25, color=(255, 127, 0, 255),
                                                           x=self.window.width // 2,
                                                           y=self.window.height // 7 * (4 - i),
                                                           anchor_x='center',
                                                           anchor_y='center',
                                                           batch=self.batch)

        @self.window.event
        def on_key_press(symbol, modifiers):
            soundtrack = pyglet.resource.media('choice.wav')
            soundtrack.play()
            if symbol == pyglet.window.key.UP:
                self.select_item = (self.select_item - 1) % len(self.items)
            elif symbol == pyglet.window.key.DOWN:
                self.select_item = (self.select_item + 1) % len(self.items)
            elif symbol == pyglet.window.key.ENTER:
                self.check_state()
            elif symbol == pyglet.window.key.BACKSPACE:
                self.done = True
                self.next = 'MENU'

    def check_state(self):
        if self.items[self.select_item] == 'FULLSCREEN':
            self.fullscreen = not self.fullscreen
            self.window.set_fullscreen(self.fullscreen,width=self.window.width, height=self.window.height)
        elif self.items[self.select_item] == 'AUDIO':
            self.audio = not self.audio
            if self.audio:
                pyglet.options['audio'] = ('openal')
            elif not self.audio:
                pyglet.options['audio'] = ('silent')
        elif self.items[self.select_item] == 'SHAKE':
            self.shake = not self.shake
            self.pos = self.window.get_location()
        elif self.items[self.select_item] == 'INITIALISE':
            self.init = True
            self.save_init()

    def save_init(self):
        p = os.path.join('resources', 'levels','complete_levels.json')
        with open(p,'r') as f:
            d = json.load(f)
        for i in d:
            q = os.path.join('resources', 'levels', 'level{}.json'.format(i))
            with open(q, 'r') as f:
                game_data = json.load(f)
            answer = ''
            for i in game_data['solution']:
                if i in game_data['cipher_dict']:
                    answer += '_'
                else:
                    answer += i
            game_data['answer'] = answer
            with open(q, 'w') as f:
                json.dump(game_data,f)
        d ={}
        with open(p,'w') as f:
            json.dump(d,f)
        
            
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
        self.title.draw()
        for i in self.labels:
            self.labels[i].color = (255, 127, 0, 255)
        self.labels[self.items[self.select_item]].color = (0, 0, 255, 255)
        self.labels['FULLSCREEN'].text ='FULLSCREEN  '+str(self.fullscreen)
        self.labels['AUDIO'].text = 'AUDIO  '+str(self.audio)
        self.labels['SHAKE'].text = 'SHAKE  '+str(self.shake)
        self.labels['INITIALISE'].text = 'INITIALISE  ' + str(self.init)
        self.batch.draw()



    def update(self,dt):
        self.window.clear()
        self.draw_background()
        self.draw_text()
        if self.shake:
            self.window.set_location(self.pos[0] + int(random.random()*10),self.pos[1] + int(random.random()*10))

