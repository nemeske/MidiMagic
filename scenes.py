from scenebase import *
from shapes import *
import pygame
import random
import colorsys


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
        screen.fill((255, 255, 0))


class GameScene(SceneBase):
    def __init__(self, width, length):
        super().__init__(width, length)
        self.note = -1
        self.vel = -1
        self.bg_h = 1.0
        self.bg_s = 1.0
        self.bg_v = 1.0

    def add_circle(self, note, vel):
        pos = [random.randint(0, self.width), random.randint(0, self.length)]
        min_note = 36
        max_note = 84
        min_vel = 0.5
        max_vel = 9
        v1 = vel / 128 * max_vel + min_vel
        v2 = v1 * random.random()
        c = int((note - min_note) * (255 / (max_note - min_note)))
        colour = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(c / 255, v1 / (max_vel + min_vel),
                                                                   v2 / (max_vel + min_vel)))
        # colour = (c, 0, 0)
        if random.random() < 0.5:
            v1 *= -1
        if random.random() < 0.5:
            v2 *= -1
        radius = 100
        width = 0
        if note % 4 == 0:
            width = 4
        self.shapes.append(Circle(self, pos, colour, [v1, v2], radius, width))

    def add_rect(self, note, vel):
        pass

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
                print(type)
                print(stuff)
                print('-----')
                self.note = note
                self.vel = vel

                # the bg colour can be changed with the potmeters
                if type == 176:
                    # leftmost
                    if note == 20:
                        self.bg_h = vel / 127.0
                    if note == 21:
                        self.bg_s = vel / 127.0
                    if note == 22:
                        self.bg_v = vel / 127.0
                # drumpad creates rectangles
                if type == 153:
                    self.add_rect(note, vel)

                # only if a key was pressed and not EOM
                if vel > 0 and type == 146:
                    self.add_circle(note, vel)

    def on_event(self, events):
        pass

    def on_draw(self, screen):
        bg_colour = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.bg_h, self.bg_s, self.bg_v))
        screen.fill(bg_colour)

        note_str = self.font.render(str(self.note), True, (0, 128, 0))
        screen.blit(note_str, (self.width / 2 - note_str.get_width() / 2, self.length / 2 - note_str.get_height() / 2))
        vel_str = self.font.render(str(self.vel), True, (0, 128, 0))
        screen.blit(vel_str, (self.width / 2 - vel_str.get_width() / 2,
                              self.length / 2 - vel_str.get_height() / 2 + note_str.get_height()))

        for s in self.shapes:
            s.draw(screen)

    def on_terminate(self):
        self.on_switchto_scene(None)
        self.quit_flag = True
        self.midi.close()
