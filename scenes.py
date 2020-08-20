from scenebase import *
from shapes import *
import pygame


class TitleScene(SceneBase):
    def __init__(self, width, length):
        super().__init__(width, length)

    def on_switchto(self):
        pass

    def on_update(self):
        pass

    def on_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.on_switchto_scene(GameScene(self.width, self.length))

    def on_draw(self, screen):
        # todo: here comes the fancy logo
        screen.fill((255, 0, 0))


SHAPE_SPEED = [1.0, 1.0]


class GameScene(SceneBase):
    def __init__(self, width, length):
        super().__init__(width, length)
        self.note = -1

    def on_switchto(self):

        self.shapes = []
        # Initializing the midi controller
        pygame.midi.init()
        i = 0
        good_list = []
        chosen = 0
        while True:
            info = pygame.midi.get_device_info(i)
            if info is None:
                break
            if info[2] == 0:  # not an input device
                i += 1
                continue
            print("device: %d" % i, info)
            good_list.append(i)
            i += 1
        if len(good_list) == 0:
            print('No MIDI devices found')
            self.on_terminate()
        elif len(good_list) == 1:
            print('connecting to device %d ...' % (good_list[0]))
            chosen = 0
        else:
            print('Too many MIDI devices found, choosing MIDI 0')
            chosen = 0
        self.midi = pygame.midi.Input(good_list[chosen])
        self.font = pygame.font.SysFont("comicsansms", 72)

    def on_update(self):
        if self.quit_flag:
            return
        # shapes part
        remove_list = []
        for s in self.shapes:
            if s.state == 'dead':
                remove_list.append(s)
        for s in remove_list:
            self.shapes.remove(s)

        for s in self.shapes:
            s.update()

        # MIDI part
        poll = self.midi.poll()
        if poll:
            while True:
                data = self.midi.read(1)
                if len(data) == 0:
                    break
                (type, note, vel, stuff) = data[0][0]
                self.note = note
                if vel > 0:
                    pos = [0, 0]
                    colour = (note, 0, 0)
                    radius = 100
                    self.shapes.append(Circle(self, pos, colour, SHAPE_SPEED, radius))

    def on_event(self, events):
        pass

    def on_draw(self, screen):
        # todo: here comes prety much a lot of thing
        screen.fill((255, 255, 0))

        text = self.font.render(str(self.note), True, (0, 128, 0))
        screen.blit(text, (self.width / 2 - text.get_width() / 2, self.length / 2 - text.get_height() / 2))

        for s in self.shapes:
            s.draw(screen)

    def on_terminate(self):
        self.on_switchto_scene(None)
        self.quit_flag = True
        self.midi.close()
