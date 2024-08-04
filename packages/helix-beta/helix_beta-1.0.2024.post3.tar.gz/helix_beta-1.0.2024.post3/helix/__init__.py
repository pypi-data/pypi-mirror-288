from .defines import *

from .gui import *
from .math import *
from .light import *
from .clock import *
from .events import *
from .components import *
from .physics import *

class HXobject:
    def __init__(
            self,
            sgrid,
        ) -> None:
        self.rect=None
        self.sgrid=sgrid
        self.dead:bool=False
        self.components:dict={}
        self.render_layer:str="background"
        sgrid.add_object(self)

    def has_component(self, component:HXcomponent) -> bool :
        if type(component) == type and self.components.get(component, False): return True
        else: return False

    def get_component(self, component:HXcomponent) -> None|HXcomponent :
        if type(component) == type:
            t = self.components.get(component, False)
            if t: return t
            else: return None
        
    def add_component(self, component:HXcomponent, *args, **kwargs):
        if type(component) == type and not self.components.get(component, False):
            self.components[component] = component(object=self, *args, **kwargs)
    
    def set_component(self, component:HXcomponent, *args, **kwargs):
        if type(component) == type and self.components.get(component, False):
            self.components[component] = component(object=self, *args, **kwargs)

    def rem_component(self, component:HXcomponent):
        if type(component) == type and self.components.get(component, False):
            self.components.pop(component)

    def update(self, *args, **kwargs):
        if not self.dead:
            [ c.update(*args, **kwargs) for c in self.components.values()]
    
    def kill(self) -> None :
        self.dead = True
    
    def free(self) -> None :
        if self.sgrid:
            self.sgrid.rem_object(self)
        
        [ c.free() for c in self.components.values() ]
        self.components.clear()
        
        self.sgrid = None

class HXsnode:
    def __init__(self, w:int, h:int, x:float|int, y:float|int) -> None:
        self.objects:list = []
        self.size:math.vec2 = math.vec2(w, h)
        self.location:math.vec2 = math.vec2(x, y)

class HXsgrid:
    def __init__(self, w: int, h: int, node_size: math.vec2) -> None:
        self.size = vec2(w, h)
        self.nodes:dict[tuple[int, int], HXsnode] = {}
        self.node_size = node_size
        self.init_nodes(w, h, node_size)
    
    def init_nodes(self, w:int, h:int, node_size:math.vec2):
        for nx in range(int(w / node_size.x)):
            for ny in range(int(h / node_size.y)):
                self.nodes[(nx, ny)] = HXsnode(
                    w=node_size.x, h=node_size.y, x=nx * node_size.x, y=ny * node_size.y)

    def get_node_ids(self, rect: pg.Rect) -> set[tuple[int, int]]:
        node_ids = set()
        top_left = (int(rect.left // self.node_size.x), int(rect.top // self.node_size.y))
        bottom_right = (int(rect.right // self.node_size.x), int(rect.bottom // self.node_size.y))
        
        for x in range(top_left[0], bottom_right[0] + 1):
            for y in range(top_left[1], bottom_right[1] + 1):
                node_ids.add((x, y))
                
        return node_ids

    def add_object(self, object: 'HXobject') -> None:
        if object.has_component(HXtransform):
            t = object.get_component(HXtransform)
            node_ids = self.get_node_ids(t.get_rect())
            for node_id in node_ids:
                n:HXsnode = self.nodes.get(node_id, None)
                if n:
                    if object not in n.objects:
                        n.objects.append(object)
                        t.spatial_ids.add(node_id)

    def rem_object(self, object: 'HXobject') -> None:
        if object.has_component(HXtransform):
            t = object.get_component(HXtransform)
            for node_id in t.spatial_ids:
                n:HXsnode = self.nodes.get(node_id, None)
                if n and object in n.objects:
                    n.objects.remove(object)
            t.spatial_ids.clear()

    def query_nodes(self, transform:HXtransform) -> list[HXsnode]:
        node_ids = self.get_node_ids(create_rect(transform.location, transform.size))
        return [self.nodes[node_id] for node_id in node_ids if node_id in self.nodes]

    def render(self, display: pg.Surface, offset):
        [pg.draw.rect(display, (255,255,255), pg.Rect(self.nodes[n].location - offset, self.nodes[n].size), 1) for n in self.nodes]

class HXcamera:
    def __init__(self, display:pg.Surface, bounds:math.vec2) -> None:
        self.zoom:float = 1.0
        self.zoom_min:float = 0.3
        self.zoom_max:float = 1.0
        self.speed:float = 1.0
        self.target:HXobject=None
        self.interpolation:float=1.0
        self.display:pg.Surface=display
        self.target_transform:HXtransform=None
        self.dw:float = display.get_width()
        """ display width """
        self.dh:float = display.get_height()
        """ display height """
        self.hdw:float = display.get_width() / 2
        """ half display width """
        self.hdh:float = display.get_height() / 2
        """ half display height """
        self.bounds:math.vec2=math.vec2(bounds)
        self.location:math.vec2 = math.vec2(100, 100)

    def get_location(self) -> math.vec2 :
        return self.location

    def set_target(self, target:HXobject):
        if type(target) == HXobject: 
            self.target = target
            if target.has_component(HXtransform):
                self.target_transform = target.get_component(HXtransform)
        else: 
            self.target = None
            self.target_transform = None

    def update(self, delta_time:float):
        self.zoom = math.clamp(self.zoom, self.zoom_min, self.zoom_max)
        
        # Calculate the new camera position
        new_pos = math.vec2(
            (self.target_transform.get_rect().centerx + self.target_transform.size[0]/2) - self.hdw * self.zoom,
            (self.target_transform.get_rect().centery + self.target_transform.size[1]/2) - self.hdh * self.zoom
        )
        
        # Apply interpolation for smooth camera movement
        self.location += ( ( (new_pos - self.location) * self.speed ) / self.interpolation ) * delta_time

        # Constrain camera within the its bounds
        self.location.x = max(0, min(self.location.x, self.bounds.x))
        self.location.y = max(0, min(self.location.y, self.bounds.y))

class HXrenderer:
    def __init__(self, number_of_layers:int):
        self.layer_array = []
        self.layers:dict = {"background":pg.sprite.Group(), "midground":pg.sprite.Group(), "foreground":pg.sprite.Group()}

    def rem_from_layer(self, object:HXobject, layer:str="background"):
        """Remove an object from a specific layer."""
        if object.has_component(HXtexture):
            self.layers[layer].remove(object.components[HXtexture])
        if object.has_component(HXanim):
            self.layers[layer].remove(object.components[HXanim])
        self.layer_array.remove(object)

    def add_to_layer(self, object:HXobject, layer:str="background"):
        """Add an object to a specific layer."""
        if object.has_component(HXtexture):
            self.layers[layer].add(object.components[HXtexture])

        if object.has_component(HXanim):
            self.layers[layer].add(object.components[HXanim])
        self.layer_array.append(object)

    def render(self, sgrid:HXsgrid, cursor:HXcursor, window:HXwindow, zoom:float, offset=pg.math.Vector2(0,0), show_colliders:bool=False, show_rects:bool=False, show_grid:bool=False, show_nodes:bool=False):
        otransform:HXtransform=None
        fill_surface(window.display, window.display_color)
        fill_surface(window.internal, window.window_color)
        
        # render grid
        if show_grid: sgrid.render(window.display, offset)

        for layer in self.layers:
            for tobject in list(self.layers[layer].sprites()):
                object = tobject.object
                if object.dead: 
                    try: self.rem_from_layer(object, object.render_layer)
                    except(ValueError): pass # double free?
                if object.has_component(HXtransform):
                    ocollider = object.get_component(HXcollider)
                    otransform = object.get_component(HXtransform)
                    
                    draw_loc = (
                        otransform.location[0]-offset[0],
                        otransform.location[1]-int(offset[1])
                    )
                    
                    if object.has_component(HXtexture):
                        tex = object.get_component(HXtexture)
                        tex.rect = otransform.get_rect(offset)
                        tex.rect.topleft = tex.rect.topleft - vec2(tex.offset)
                        
                        window.display.blit(flip_surface(tex.image, otransform.negx, False), vec2(tex.rect.topleft)-vec2(tex.offset))
                    
                    if object.has_component(HXanim):
                        anim = object.get_component(HXanim)
                        if (anim.texture):
                            anim.texture.rect = otransform.get_rect(offset)
                            anim.texture.rect.topleft = anim.rect.topleft - vec2(anim.texture.offset)
                        
                        window.display.blit(flip_surface(anim.image, otransform.negx, False), vec2(draw_loc)-vec2(anim.frames[int(anim.nframe)].offset))
                    
                    if show_nodes:
                        onodes = sgrid.query_nodes(otransform)
                        [ gui.draw_rect(window.display, node.size, (node.location-offset)) for node in onodes if onodes ]
            
                    if show_rects: gui.draw_rect(window.display, otransform.size, draw_loc, color=[255, 255, 255], width=2)
            
                    if show_colliders and ocollider: 
                        draw_rect(window.display, ocollider.rect.size, ocollider.rect.topleft-offset, [0, 255, 0], width=1)

        window.internal.blit(
            gui.scale_surface(window.display, [ window.dimensions[0]/zoom, window.dimensions[1]/zoom ]),
            [0,0]
        )

        # render cursor
        cursor.render(window.internal, offset)
              
        pg.display.flip()

from .version import *
if "HELIX_HIDE_PROMPT" not in os.environ:
    print(f"Helix {HELIX_MAJOR_VER}.{HELIX_MINOR_VER}.{HELIX_PATCH_VER}+{HELIX_YR_EDITION}\n")

