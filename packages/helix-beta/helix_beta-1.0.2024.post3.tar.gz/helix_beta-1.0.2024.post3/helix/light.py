from .defines import *

class HXpointlight2D:
    def __init__(self, location:list[int|float], color=[55,55,55], brightness=1, radius=1, step=1, alpha=1) -> None:
        self.step:int=step
        self.alpha:int=alpha
        self.radius:int=radius
        self.image:pg.Surface=None
        self.color:list[int]=color
        self.brightness:int=brightness
        self.location:list[int|float]=location
        self.cycle:list[pg.Surface]=[
            point_light_2D(radius, brightness, color)
            for radius in range(radius, radius*2)
        ]
        self.cycle_reverse:list[pg.Surface]=self.flicker_cycle.copy().reverse()

        self.accumulator:float=0.0
        self.flicker_indeces = [random.randint(0, (len(self.cycle) - 1) * 2)]

    def update(self, dt):
        self.accumulator += dt
        self.flicker_indeces = [random.randint(0, (len(self.cycle) - 1) * 2)]
        if self.accumulator >= 0.05:
            for index, flicker_index in enumerate(self.flicker_indeces):
                max_index = (len(self.flicker_cycle) - 1) * 2
                if flicker_index < max_index:
                    self.flicker_indeces[index] += 1
                else:
                    self.flicker_indeces[index] = random.randint(0, max_index)
                    if random.random() < 0.1:
                        self.flicker_indeces[index] = random.randint(0, max_index)
            self.accumulator = 0

    def render(self, display, offset=(0,0), zoom=(0,0)):
        for i in range(len(self.flicker_indeces)):
            flicker_index = self.flicker_indeces[i]
            if flicker_index > len(self.flicker_cycle) - 1:
                cycle_list = self.reversed_flicker_cycle
                index = flicker_index - len(self.flicker_cycle) + 1
            else:
                cycle_list = self.flicker_cycle
                index = flicker_index
            self.image = cycle_list[index]
            self.rect = pg.Rect(self.location, self.image.get_size())
        display.blit(self.image, (0, 0), special_flags=pg.BLEND_RGB_MULT)


def point_light_2D(color=[55,55,55], brightness=1, radius=1, step=1, alpha=1) -> pg.Surface:
    # make a surface the size of the largest circle's diameter (radius * 2)
    surface = pg.Surface((int(radius) * 2, int(radius) * 2), pg.SRCALPHA)
    surface.convert_alpha()

    currentRadius = radius
    circleCount = radius // step

    # for every circle in circleCount
    for layer in range(circleCount):

        # create a new surface for the new circle (same size as original)
        layerSurface = pg.Surface((int(radius) * 2, int(radius) * 2), pg.SRCALPHA)
        layerSurface.convert_alpha()
        layerSurface.set_alpha(alpha)

        # draw the new circle on the new surface using the currentRadius
        pg.draw.circle(layerSurface, [(brightness/100) * value for value in color], (radius, radius), currentRadius, width=5)  # width determines how much each circle overlaps each other

        # blit the circle layer onto the main surface
        surface.blit(layerSurface, (0, 0))

        # update the currentRadius and alpha for the next circle layer
        currentRadius -= step
        alpha += 1

    # return the main surface that has all the circle layers drawn on it
    return surface

class HXpointlight2D_2:
    def __init__(self, location:list, brightness_color, flicker_cycle, reversed_flicker_cycle):
        # Initialize the HXpointlight2D object with provided parameters
        self.location = location
        self.flicker_accumulator = 0  # Flicker accumulator for timing
        self.flicker_cycle = flicker_cycle  # List of flicker images
        self.brightness_color = brightness_color  # Color for world brightness
        self.reversed_flicker_cycle = reversed_flicker_cycle  # List of reversed flicker images
        self.flicker_indeces = [random.randint(0, (len(flicker_cycle) - 1) * 2)]   # Random flicker indices

    def update(self, dt):
        # Update the HXpointlight2D object
        self.flicker_accumulator += dt  # Increment the flicker accumulator by the time step
        if self.flicker_accumulator >= 0.04:
            for index, flicker_index in enumerate(self.flicker_indeces):
                max_index = (len(self.flicker_cycle) - 1) * 2
                if flicker_index < max_index:
                    self.flicker_indeces[index] += 1
                else:
                    self.flicker_indeces[index] = random.randint(0, max_index)
                    if random.random() < 0.1:
                        self.flicker_indeces[index] = random.randint(0, max_index)
            self.flicker_accumulator = 0  # Reset the flicker accumulator

    def render(self, surface, offset=(0,0), zoom=(0,0)):
        # Create a surface for world brightness
        world_brightness = pg.Surface(
            pg.math.Vector2(surface.get_size()[0] * zoom, surface.get_size()[1] * zoom),
            pg.SRCALPHA,
        ).convert_alpha()
        world_brightness.fill(self.brightness_color)  # Fill the surface with the specified brightness color

        for i in range(len(self.flicker_indeces)):
            flicker_index = self.flicker_indeces[i]
            if flicker_index > len(self.flicker_cycle) - 1:
                cycle_list = self.reversed_flicker_cycle
                index = flicker_index - len(self.flicker_cycle) + 1
            else:
                cycle_list = self.flicker_cycle
                index = flicker_index
            light = cycle_list[index]  # Get the current light image
            rect = light.get_rect()
            world_brightness.blit(light, rect)  # Blit the light onto the world brightness surface

        surface.blit(world_brightness, (0, 0), special_flags=pg.BLEND_RGB_MULT)  # Render the world brightness onto the main surface

