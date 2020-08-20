import pygame
import pygame.midi
from scenes import *


def run_game(width, height, fps, starting_scene):
    pygame.init()
    pygame.display.set_caption('MidiMagic')
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
    width = 1024
    length = 768
    fps = 60
    run_game(width, length, fps, TitleScene(width, length))
