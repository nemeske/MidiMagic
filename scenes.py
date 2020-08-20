from scenebase import *
import pygame


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def on_switchto(self):
        pass

    def on_update(self):
        pass

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.on_switchto_scene(GameScene())

    def on_draw(self, screen):
        # todo: here comes the fancy logo
        screen.fill((255, 0, 0))


class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def on_switchto(self):
        # Initializing the midi controller

    def on_update(self):
        pass

    def on_event(self, events):
        pass

    def on_draw(self, screen):
        # todo: here comes prety much a lot of thing
        screen.fill((255, 255, 0))
