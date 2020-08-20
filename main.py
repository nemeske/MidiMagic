import pygame
import pygame.midi
from scenes import *


def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.on_terminate()
            else:
                filtered_events.append(event)

        active_scene.on_event(filtered_events)
        active_scene.on_update()
        active_scene.on_draw(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    run_game(400, 300, 60, TitleScene())

    # pygame.init()
    # pygame.midi.init()
    # i = 0
    # good_list = []
    # chosen = 0
    # while True:
    #     info = pygame.midi.get_device_info(i)
    #     if info == None:
    #         break
    #     if info[2] == 0:  # not an input device
    #         i += 1
    #         continue
    #     print("device: %d" % i, info)
    #     good_list.append(i)
    #     i += 1
    # if len(good_list) == 0:
    #     print('No MIDI devices found')
    #     #self.director.change_scene(None, [])
    #     # TODO: break here
    # elif len(good_list) == 1:
    #     print('connecting to device %d ...' % (good_list[0]))
    #     chosen = 0
    # else:
    #     print('Too many MIDI devices found, choosing MIDI 0')
    #     chosen = 0
    # midi = pygame.midi.Input(good_list[chosen])


    # while True:
    #     poll = midi.poll()
    #     if poll == True:
    #         print('Polled')
    #         while True:
    #             data = midi.read(1)
    #             if len(data) == 0:
    #                 break
    #             (type, note, vel, stuff) = data[0][0]
    #             print('Read note')
    #             print(type)
    #             print(note)
    #             print(vel)
    #             print(stuff)

    # Closing midi
    # print('Closing MIDI')
    # midi.close()