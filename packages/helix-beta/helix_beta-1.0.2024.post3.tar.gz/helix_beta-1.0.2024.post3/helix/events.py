from .defines import *
from .gui import *
from .math import *

class HXcursor:
    def __init__(self) -> None:
        self.winpos:pg.math.Vector2=vec2()
        self.gridpos:pg.math.Vector2=vec2()
        self.image:pg.Surface=load_image(f"{HXASSET_DIR}cursor.png")
    
    def render(self, display:pg.Surface, offset:list[int|float]):
        display.blit(self.image, self.winpos)
    
    def update(self, zoom:float, offset:list[float|int]):
        self.winpos = vec2(pg.mouse.get_pos())

        self.gridpos = vec2(
            ( pg.mouse.get_pos()[0] * zoom ) + offset[0],
            ( pg.mouse.get_pos()[1] * zoom ) + offset[1]
        )

class HXevents:
    def __init__(self):
        self.keyboard = {}
        self.mouse_pos = (0,0)
        self.mouse_delta = (0,0)
        self.kb_state = []
        self.mouse_state = []
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0
        self.mouse = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False}
        
        self.mouse_wheelu=False
        self.mouse_wheeld=False
        self.mouse_prev = {}
        self.keyboard_prev = {}
        
        self.controllers = {}
        self.controller_name = None
        self.controller = None
        self._controller_max = 25
    
    def register_controller(self, name, controller):
        if len(list(self.controllers.keys())) + 1 < self._controller_max:
                if name not in self.controllers:
                    self.controllers[name] = controller
                    self.controller_name = name
                    self.controller = self.controllers[self.controller_name]
    
    def set_controller(self, name):
        if name in self.controllers:
            self.controller_name = name
            self.controller = self.controllers[self.controller_name]
    
    def rem_controller(self, name):
        if name in self.controllers:
            self.controllers.pop(name)
            index = len(list(self.controllers.keys())) - 1
            self.controller_name = list(self.controllers.keys())[index]
            self.controller = self.controllers[self.controller_name]

    def process(self) -> int:
        self.mouse_wheelu = False
        self.mouse_wheeld = False
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_prev = self.mouse.copy()
        self.mouse_delta = pg.mouse.get_rel()
        self.keyboard_prev = self.keyboard.copy()
        self.kb_state = pg.key.get_pressed()
        self.mouse_state = pg.mouse.get_pressed()
        self.mouse_dx, self.mouse_dy = self.mouse_delta
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F12):
                return 1
            match event.type:
                case pg.KEYUP:
                    self.keyboard[event.key] = False
                case pg.KEYDOWN:
                    self.keyboard[event.key] = True
                case pg.MOUSEBUTTONUP:
                    self.mouse[event.button] = False
                case pg.MOUSEBUTTONDOWN:
                    self.mouse[event.button] = True
                    if event.button == 4:
                        self.mouse_wheelu = True
                    if event.button == 5:
                        self.mouse_wheeld = True
        self.controller() if self.controller else 0

    def is_key_pressed(self, key):
        return self.keyboard.get(key, False)

    def is_key_triggered(self, key):
        return self.keyboard.get(key, False) and not self.keyboard_prev.get(key, False)
    
    def is_mouse_pressed(self, button:int):
        return self.mouse.get(button, False)

    def is_mouse_triggered(self, button):
        return self.mouse.get(button, False) and not self.mouse_prev.get(button, False)
    
