import pygame
import pygame.midi


def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((240, 180))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

if __name__ == "__main__":
    # Init
    #pygame.init()
    pygame.midi.init()
    i = 0
    good_list = []
    chosen = 0
    while True:
        info = pygame.midi.get_device_info(i)
        if info == None:
            break
        if info[2] == 0:  # not an input device
            i += 1
            continue
        print("device: %d" % i, info)
        good_list.append(i)
        i += 1
    if len(good_list) == 0:
        print('No MIDI devices found')
        #self.director.change_scene(None, [])
        # TODO: break hera
    elif len(good_list) == 1:
        print('connecting to device %d ...' % (good_list[0]))
        chosen = 0
    else:
        print('Too many MIDI devices found, choosing MIDI 0')
        chosen = 0
    midi = pygame.midi.Input(good_list[chosen])


    while True:
        poll = midi.poll()
        if poll == True:
            print('Polled')
            while True:
                data = midi.read(1)
                if len(data) == 0:
                    break
                (type, note, vel, stuff) = data[0][0]
                print('Read note')
                print(type)
                print(note)
                print(vel)
                print(stuff)

    # Closing midi
    print('Closing MIDI')
    midi.close()

    #main()