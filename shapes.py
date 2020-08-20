import pygame


class Shape(object):
    def __init__(self, parent, pos, colour, velocity):
        self.parent = parent
        self.pos = pos
        self.colour = colour
        self.velocity = velocity
        self.state = 'alive'

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        if self.pos[0] > self.parent.width or self.pos[1] > self.parent.length \
                or self.pos[0] < 0 or self.pos[1] < 0:
            self.state = 'dead'

    def draw(self):
        raise NotImplementedError("draw abstract method must be defined in subclass.")


class Circle(Shape):
    def __init__(self, parent, pos, colour, velocity, radius, width=0):
        super().__init__(parent, pos, colour, velocity)
        self.radius = radius
        self.width = width

    def draw(self, surface):
        if self.state == 'alive':
            pygame.draw.circle(surface, self.colour, (int(self.pos[0]), int(self.pos[1])), self.radius, self.width)
