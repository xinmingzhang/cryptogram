import pyglet

FPS = 60.0
WIDTH = 800
HEIGHT = 600

pyglet.resource.path = ['resources',
                        'resources/fonts',
                        'resources/graphics',
                        'resources/music',
                        'resources/sound']
pyglet.resource.reindex()

pyglet.resource.add_font('Yonezawa.ttf')


# pyglet.font.add_file('resources/fonts/Yonezawa.ttf')
pyglet.font.load('Yonezawa',dpi = 96)

