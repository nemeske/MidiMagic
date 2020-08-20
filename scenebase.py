class SceneBase(object):
    def __init__(self):
        self.next = self

    def on_switchto(self):
        raise NotImplementedError("on_switchto abstract method must be defined in subclass.")

    def on_update(self):
        raise NotImplementedError("on_update abstract method must be defined in subclass.")

    def on_event(self, events):
        raise NotImplementedError("on_event abstract method must be defined in subclass.")

    def on_draw(self, screen):
        raise NotImplementedError("on_draw abstract method must be defined in subclass.")

    def on_switchto_scene(self, next_scene):
        self.next = next_scene
        next_scene.onswitchto()

    def on_terminate(self):
        self.on_switchto_scene(None)
