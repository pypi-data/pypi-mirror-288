from .defines import *
from .gui import *
from .math import *

# Base component class
# --------------------------- #
class HXcomponent(pg.sprite.Sprite):
    def __init__(self, object, *groups) -> None:
        super().__init__(*groups)
        self.object = object
        self.image = pg.Surface([0,0])
        self.rect = pg.Rect([0,0], [0,0])
    def update(self, *args, **kwargs): raise NotImplementedError
    def free(self, *args, **kwargs): raise NotImplementedError
# --------------------------- #

# --------------------------- #
class HXtransform:
    def __init__(self, object, size:list[int]=[32, 32], location:list[int]=[100, 100]) -> None :
        self.object = object
        self.dynamic:bool=False
        self.negx:bool=False
        self.mass:float=10.0
        self.scale:float=1.0
        self.speed:float=120.0
        self.rotation:float=0.0
        self.size:pg.math.Vector2=vec2(size)
        self.velocity:pg.math.Vector2=vec2()
        self.location:pg.math.Vector2=vec2(location)
        self.center:pg.math.Vector2=vec2(self.location[0]+(self.size[0]//2), self.location[1]+(self.size[1]//2))
        
        self.sgrid = object.sgrid
        self.spatial_ids = set()
        if self.sgrid:
            self.sgrid.add_object(self.object)

    
    def get_spatial_ids(self) -> set:
        return self.spatial_ids

    def get_rect(self, offset:pg.math.Vector2=vec2(0,0)) -> pg.Rect:
        return pg.Rect(self.location - offset, self.size)

    def set_scale(self, scale:float=1.0) -> None :
        self.scale = scale
        
    def set_speed(self, speed:float=120.0) -> None :
        self.speed = speed

    def set_velocity(self, x:float|int=0.0, y:float|int=0.0, vec:pg.math.Vector2=None) -> None :
        if vec: self.velocity = vec
        else:
            self.velocity.x = x
            self.velocity.y = y

    def move(self, delta_time:float, up:bool=False, down:bool=False, left:bool=False, right:bool=False):
        if up: self.velocity[1] = -self.speed
        if down: self.velocity[1] = self.speed
        if left: self.velocity[0] = -self.speed
        if right: self.velocity[0] = self.speed

    def update_spatial_ids(self) -> None:
        if self.sgrid:
            new_spatial_ids = self.sgrid.get_node_ids(self.get_rect())
            if new_spatial_ids != self.spatial_ids:
                self.sgrid.rem_object(self.object)
                self.spatial_ids = new_spatial_ids
                self.sgrid.add_object(self.object)

    def update(self, delta_time:float, *args, **kwargs) -> None:
        self.center = vec2(self.location[0] + (self.size[0] // 2), self.location[1] + (self.size[1] // 2))
        self.update_spatial_ids()

    def free(self):
        self.velocity = None
        self.location = None
        self.size = None
        self.center = None
        if self.sgrid:
            self.sgrid.rem_object(self.object)
        self.sgrid = None
        self.spatial_ids.clear()
# --------------------------- #

# --------------------------- #
class HXtexture(HXcomponent):
    def __init__(self, object, size:list[int]=[32, 32], color:list[int]=[25, 60, 80], path:str=None, render_layer:str="background", offset:list[int]=[0,0]):
        super().__init__(object, [])
        self.flip_x:bool=False
        self.flip_y:bool=False
        self.size:list[int]=size
        self.color:list[int]=color
        self.offset:list[int]=offset
        self.render_layer:str=render_layer
        if path: 
            self.load(path)
        else:
            self.image:pg.Surface=pg.Surface(self.size)
            self.image.fill(self.color)
    
    def set(self, texture:pg.Surface) -> None :
        self.image = texture
    
    def load(self, path:str) -> None :
        self.image = load_image(path)

    def flip(self, x:bool, y:bool):
        self.image = flip_surface(self.image, x, y)

    def scale(self, scale:list) -> None :
        self.size = scale
        self.image = scale_surface(self.image, scale)

    def rotate(self, angle:float) -> None :
        self.image = rotate_surface(self.image, angle)
    
    def update(self, *args, **kwargs) -> None : ...
    
    def free(self):
        self.image = None
        self.size = None
        self.color = None
# --------------------------- #

# --------------------------- #
class HXanim(HXcomponent):
    def __init__(self, object, flip_speed:float, dimensions:list[int], image_offset:list[int]=[0,0], loop:bool=False, loop_delay:bool=False, delay:int|float=4, scale:list[int]=[1,1], sheet_path:str=None, dir_path:str=None):
        super().__init__(object, [])
        self.nframe:int = 0
        """ number of current frame """
        self.nframes:int = 0
        """ number of total frames """
        self.texture:HXtexture = None
        """ current frame texture """
        self.image:HXtexture = None
        """ current frame image """
        self.frames:list[pg.Surface] = []
        """ array of frame images """
        self.flip_speed:float = flip_speed
        """ the speed of iteration of frame images """
        self.dimensions:list[int] = dimensions
        """ dimensions of a frame """
        self.acc:float=0.0
        self.ldtime:float=delay
        """ amount of time a frame should be displayed """
        self.loop:bool = loop
        """ flag to control animation looping """
        self.loop_delay:bool=loop_delay

        self.src:str=None

        self.image_offset:list[int]=image_offset

        if self.loop == True:
            self.loop_delay = False
        
        if self.loop_delay == True:
            self.loop = False
        
        if dir_path != None:
            self.load_dir(dir_path, dimensions)
        if sheet_path != None:
            self.load_sheet(sheet_path, dimensions, scale) 
        
    def load_dir(self, dir_path:str, dimensions:list[int]): ...
    
    def load_sheet(self, sheet_path:str, dimensions:list[int], scale:list[int]=[1,1]):
        frame_images = load_image_sheet(sheet_path, dimensions)
        frame_textures = [HXtexture(self.object, dimensions, offset=self.image_offset) for _ in frame_images]
        [ frame_textures[t].set(tex) for t, tex in enumerate(frame_images) ]
        [ frame_textures[t].scale([self.dimensions[0]*scale[0], self.dimensions[1]*scale[1]]) for t, _ in enumerate(frame_images)]
        self.nframe = 0
        self.frames = frame_textures
        self.nframes = len(self.frames)
        self.image = self.frames[int(self.nframe)].image
        self.src = sheet_path
    
    def update(self, delta_time:float, *args, **kwargs) -> None :
        if self.nframes <= 0: return

        self.acc+=1*delta_time
        self.nframe += self.flip_speed * delta_time

        if self.loop:
            self.nframe %= self.nframes # loop: wrap around using modulo
        
        elif self.loop_delay: # delay the loop by the amount of frame time set
            if self.nframe >= self.nframes - 1:
                if int(self.acc) == self.ldtime:
                    self.nframe = 0 # loop: wrap around using modulo
                    self.acc = 0
                else: self.nframe = self.nframes - 1
        
        else: # no-loop: clamp to last frame
            if self.nframe >= self.nframes - 1:
                self.nframe = self.nframes - 1
            elif self.nframe < 0:   # bounds check
                self.nframe = 0
        
        self.texture = self.frames[int(self.nframe)]
        self.image = self.texture.image
    
    def free(self):
        self.frames = None
        self.image = None
        self.dimensions = None
# --------------------------- #

# --------------------------- #
class HXliferange(HXcomponent):
    def __init__(self, object, scalar:int|float=1.0, lifetime:int|float=None, range:int|float=None) -> None :
        super().__init__(object, [])
        self.scalar:int|float = scalar
        self.liferange = lifetime if lifetime != None else range
    
    def free(self) -> None :
        self.scalar = None
        self.liferange = None
    
    def update(self, delta_time:float, *args, **kwargs) -> None :
        self.liferange -= self.scalar * delta_time
        if self.liferange <= 0: 
            self.object.kill()
# --------------------------- #

# --------------------------- #
class HXcollider(HXcomponent):
    def __init__(self, object, dimensions:list[int]):
        super().__init__(object, [])
        self.dimensions:list[int]=dimensions
        self.rect:pg.Rect = pg.Rect([0, 0], dimensions)
        self.transform:HXtransform=self.object.get_component(HXtransform)
        self.colliding = {
            "top":False,
            "left":False,
            "right":False,
            "bottom":False
        }
        self.grounded = 10
        self.update()

    def update(self, *args, **kwargs):
        self.rect.topleft = self.transform.location
# --------------------------- #

# --------------------------- #
class HXactiongraph(HXcomponent):
    def __init__(self, object) -> None:
        super().__init__(object=object)
        self.action:str=None
        self.nactions:int=0
        self.ncallbacks:int=0
        self.conditions:dict[str, bool]={}
        self.actions:dict[str, callable]={}

    def run_action(self, action:str) -> None:
        if self.action != action:
            self.action = action
            try:
                self.get_action(action=action)()
            except (AttributeError) as err: action=None; print(err) # action has no registered callback

    def get_action(self, action:str) -> None:
        callback:callable = None
        try:
            callback = self.actions.get(action, None)
        except (KeyError) as err: print(err)  # action not registered
        return callback

    def rem_action(self, action:str) -> None:
        try:
            self.actions.pop(key=action)
        except (KeyError) as err: print(err) # action not registered

    def add_action(self, action:str, callback:callable) -> None:
        if not self.get_action(action=action):
            self.actions[action] = callback
        else: ... # action already registered

    def set_action(self, action:str, callback:callable) -> None:
        if self.get_action(action=action):
            self.actions[action] = callback
        else: ... # action not registered

    def try_condition(self, con:str) -> bool:
        try:
            return self.get_condition(con=con)()
        except (AttributeError) as err: print(err); return False # action has no registered callback

    def get_condition(self, con:str) -> None:
        callback:callable = None
        try:
            callback = self.conditions.get(con, None)
        except (KeyError) as err: print(err)  # action not registered
        return callback

    def rem_condition(self, con:str) -> None:
        try:
            self.conditions.pop(key=con)
        except (KeyError) as err: print(err) # action not registered

    def add_condition(self, con:str, callback:callable) -> None:
        if not self.get_condition(con=con):
            self.conditions[con] = callback
        else: ... # action already registered

    def set_condition(self, con:str, callback:callable) -> None:
        if self.get_condition(con=con):
            self.conditions[con] = callback
        else: ... # action not registered

    def update(self, *args, **kwargs) -> None:
        for con in self.conditions.keys():
            if self.try_condition(con):
                self.run_action(con)
# --------------------------- #
