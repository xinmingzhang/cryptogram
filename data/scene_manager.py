

class Scene(object):
    def __init__(self,window):
        self.window = window
        self.done = False
        self.next = None

    def entry_actions(self,persist):
        self.persist = persist

    def update(self):
        pass

    def exit_data(self):
        return self.persist
    
class SceneManager(object):
    def __init__(self,window,**kwargs):
        self.scenes = kwargs
        self.current_scene = None
        self.window = window

    def set_first_scene(self,name):
        self.current_scene = self.scenes[name](window = self.window)

    def update(self,dt):
        if self.current_scene.done == True:
            if hasattr(self.current_scene, 'persist'):
                persist = self.current_scene.exit_data()                
                self.current_scene = self.scenes[self.current_scene.next](window = self.window)
                self.current_scene.entry_actions(persist)
            else:
                self.current_scene = self.scenes[self.current_scene.next](window = self.window)
        self.current_scene.update(dt)


        
