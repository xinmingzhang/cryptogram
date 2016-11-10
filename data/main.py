import sys
import pyglet
from . import scene_manager,prepare

from .states import menu
from .states import gameplay
from .states import instr
from .states import level
from .states import option


def main():
    window = pyglet.window.Window(width = prepare.WIDTH, height = prepare.HEIGHT, resizable = True, caption = 'cryptogram')
    scene_dict = {'MENU':menu.Menu,
                  'LEVEL':level.LevelChoose,
                  'INSTR':instr.Instruction,
                  'OPTION':option.Option,
                  'GAME':gameplay.GamePlay}
    scenes = scene_manager.SceneManager(window = window,**scene_dict)
    scenes.set_first_scene('MENU')
    pyglet.clock.schedule_interval(scenes.update, 1/prepare.FPS)
    pyglet.app.run()
    sys.exit()
