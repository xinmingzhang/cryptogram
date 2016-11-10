import os
import json
import pyglet
from .. import scene_manager


class GamePlay(scene_manager.Scene):
    def __init__(self, window):
        super(GamePlay, self).__init__(window)
        self.window = window
        

        self.win_label = pyglet.text.Label('LEVEL COMPLETE', font_name='Yonezawa', font_size=60,
                                           color=(127, 255, 0, 255),
                                           x=self.window.width // 2, y=self.window.height // 4 * 3, anchor_x='center',
                                           anchor_y='center', width=self.window.width, multiline=True, align='center')

        self.hint_time = 3

        self.i = 0

        self.correct_effect = 0
        self.wrong_effect = 0

        self.mark_position = 0

        self.done = False

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.RIGHT:
                self.change_position(1)
            elif symbol == pyglet.window.key.LEFT:
                self.change_position(-1)
            elif symbol == pyglet.window.key.SPACE:
                if '_' in self.answer:
                    self.get_hint()
                else:
                    pass
            elif symbol == pyglet.window.key.BACKSPACE:
                self.auto_save()
                self.done = True
                self.next = 'LEVEL'
            elif symbol == pyglet.window.key.ENTER:
                self.auto_save()
                if '_' in self.answer:
                    pass
                else:
                    self.done = True
                    self.next = 'LEVEL'
                    

            elif symbol in range(97, 123):
                self.input_letter = chr(symbol).upper()
                self.check_input(self.input_letter)

    def auto_save(self):
        data ={}
        data['puzzle'] = self.puzzle
        data['solution'] = self.solution
        data['cipher_dict'] = self.cipher_dict
        data['answer'] = self.answer
        p = os.path.join('resources', 'levels', 'level{}.json'.format(self.persist))
        with open(p,'w') as f:
            json.dump(data,f)
        



    def entry_actions(self, persist):
        self.persist = persist
        p = os.path.join('resources', 'levels', 'level{}.json'.format(self.persist))
        with open(p, 'r') as f:
            d = json.load(f)

        self.answer = d['answer']
        self.cipher_dict = d['cipher_dict']
        self.puzzle = d['puzzle']
        self.solution = d['solution']
        self.wrong_answer = self.answer
        if len(self.solution) >= 200:
            self.font = 15
        else:
            self.font = 20
        if self.answer[self.mark_position]!='_':
            self.change_position(1)

    def get_hint(self):
        if self.hint_time > 0:
            hint_sound = pyglet.resource.media('hint.wav')
            hint_sound.play()
            self.check_input(self.cipher_dict[self.puzzle[self.mark_position]])
            self.hint_time -= 1
        else:
            return

    def change_position(self, num):
        if '_' not in self.answer:
            victory_sound = pyglet.resource.media('victory.wav')
            victory_sound.play()
            p = os.path.join('resources', 'levels','complete_levels.json')
            with open(p,'r') as f:
                d = json.load(f)
            d[self.persist]=0
            with open(p,'w') as f:
                json.dump(d,f)
            return

        self.mark_position = (self.mark_position + num) % len(self.puzzle)
        if self.answer[self.mark_position] != '_':
            self.change_position(num)

    def same_letters(self, pos):
        letter = self.puzzle[pos]
        same_letters_position = []
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == letter:
                same_letters_position.append(i)
        return same_letters_position

    def answer_update(self, letter):
        string = ''
        for i in range(len(self.answer)):
            if i in self.same_letters(self.mark_position):
                string += letter
            else:
                string += self.answer[i]
        return string

    def check_input(self, letter):
        letter_in_puzzle = self.puzzle[self.mark_position]
        if letter == self.cipher_dict[letter_in_puzzle]:
            correct_sound = pyglet.resource.media('correct.wav')
            correct_sound.play()
            self.correct_effect = 255
            self.answer = self.answer_update(letter)
            self.change_position(1)

        elif letter != self.cipher_dict[letter_in_puzzle]:
            error_sound = pyglet.resource.media('error.wav')
            error_sound.play()
            self.wrong_effect = 255
            self.wrong_answer = self.answer_update(letter)

    def draw_background(self):
        self.window.clear()

        if self.i < 255:
            self.i += 5
            if self.i >= 255:
                self.i = 255

        if self.correct_effect:
            self.correct_effect -= 25
            if self.correct_effect <= 0:
                self.correct_effect = 0

        if self.wrong_effect:
            self.wrong_effect -= 25
            if self.wrong_effect <= 0:
                self.wrong_effect = 0

        a = self.i
        b = self.correct_effect
        c = self.wrong_effect

        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2i', (
                                 0, 0, self.window.width, 0, self.window.width, self.window.height, 0,
                                 self.window.height)),
                             ('c3B', (
                                 127 + a // 2, 255, 0, 127 + a // 2, 255, 0, 255 - b // 2, 255 - c // 2, 255 - b - c,
                                 255 - b // 2, 255 - c // 2, 255 - b - c)))

    def draw_text(self):
        self.p_text = pyglet.text.document.FormattedDocument(self.puzzle)
        self.a_text = pyglet.text.document.FormattedDocument(self.answer)
        self.w_text = pyglet.text.document.FormattedDocument(self.wrong_answer)

        self.p_text.set_style(0, len(self.p_text.text),
                              dict(color=(0, 0, 255, 255), font_name='Yonezawa', font_size=self.font))
        self.a_text.set_style(0, len(self.a_text.text),
                              dict(color=(0, 0, 255, 255), font_name='Arial', font_size=self.font))
        self.w_text.set_style(0, len(self.w_text.text),
                              dict(color=(0, 0, 255, 255), font_name='Arial', font_size=self.font))

        for i in range(len(self.answer)):
            if self.answer[i] != '_':
                self.a_text.set_style(i, i + 1, dict(color=(127, 255, 0, 255), font_name='Arial', font_size=self.font))
                self.w_text.set_style(i, i + 1, dict(color=(127, 255, 0, 255), font_name='Arial', font_size=self.font))

        if '_' in self.answer:
            for i in self.same_letters(self.mark_position):
                self.p_text.set_style(i, i + 1, dict(background_color=(0, 200, 0, 32)))
                self.a_text.set_style(i, i + 1, dict(background_color=(0, 200, 0, 32)))
                self.w_text.set_style(i, i + 1, dict(background_color=(0, 200, 0, 32)))
                self.w_text.set_style(i, i + 1, dict(color=(255, 127, 0, 255)))

            self.p_text.set_style(self.mark_position, self.mark_position + 1, dict(background_color=(0, 255, 0, 128)))
            self.a_text.set_style(self.mark_position, self.mark_position + 1, dict(background_color=(0, 255, 0, 128)))
            self.w_text.set_style(self.mark_position, self.mark_position + 1, dict(background_color=(0, 255, 0, 128)))

        self.p_text.set_paragraph_style(0, len(self.p_text.text),
                                        dict(leading=10, margin_left=50, margin_right=50, margin_top=50))
        self.a_text.set_paragraph_style(0, len(self.a_text.text),
                                        dict(leading=10, margin_left=50, margin_right=50, margin_top=50))
        self.w_text.set_paragraph_style(0, len(self.w_text.text),
                                        dict(leading=10, margin_left=50, margin_right=50, margin_top=50))

        self.puzzle_text = pyglet.text.layout.TextLayout(self.p_text, self.window.width, self.window.height,
                                                         dict(multiline=True))
        self.answer_text = pyglet.text.layout.TextLayout(self.a_text, self.window.width, self.window.height // 2,
                                                         dict(multiline=True))
        self.wrong_answer_text = pyglet.text.layout.TextLayout(self.w_text, self.window.width, self.window.height // 2,
                                                               dict(multiline=True))

        if '_' in self.answer:
            self.puzzle_text.draw()
        else:
            self.win_label.text = 'LEVEL {} COMPLETE'.format(self.persist)
            self.win_label.draw()

        if self.wrong_effect:
            self.wrong_answer_text.draw()
        else:
            self.answer_text.draw()

    def update(self, dt):
        self.window.clear()
        self.draw_background()
        self.draw_text()
