from .defines import *
from .math import *
from .components import HXtransform, HXcollider

# --------------------------- #
class HXphysics:
    GRAVITY:float|int = 1350
    FRICTION:float|int = 800
    def __init__(self) -> None: ...

    def set_gravity(self, g:float|int) -> None: self.GRAVITY = g
    
    def set_friction(self, f:float|int) -> None: self.FRICTION = f
    
    def gravity(self, ent, dt):
        t1 = ent.get_component(HXtransform)
        if t1.dynamic:
            t1.velocity[1] += self.GRAVITY * dt

    def friction(self, ent, dt) -> None:
        t1 = ent.get_component(HXtransform)
        if t1.velocity.x > 0:
            t1.velocity.x -= (self.FRICTION) * dt
            if t1.velocity.x < 0:
                t1.velocity.x = 0

        if t1.velocity.x < 0:
            t1.velocity.x += (self.FRICTION) * dt
            if t1.velocity.x > 0:
                t1.velocity.x = 0

    def aabby(self, check, against) -> bool:
        res:bool=False
        c1 = check.get_component(HXcollider)
        t1 = check.get_component(HXtransform)
        for ent in against:
            if ent != check:
                c2 = ent.get_component(HXcollider)
                if c1.rect.colliderect(c2.rect):
                    if t1.velocity[1] > 0:
                        t1.velocity[1] = 0
                        c1.grounded = 3
                        t1.location.y = c2.rect.top - c1.rect.height
                    elif t1.velocity[1] < 0:
                        t1.velocity[1] = 0
                        t1.location.y = c2.rect.bottom
                    res = True
        return res

    def aabbx(self, check, against) -> bool:
        res:bool=False
        c1:HXcollider = check.get_component(HXcollider)
        t1 = check.get_component(HXtransform)
        for ent in against:
            if ent != check:
                c2:HXcollider = ent.get_component(HXcollider)
                if c1.rect.colliderect(c2.rect):
                    if t1.velocity[0] > 0:
                        t1.velocity[0] = 0
                        t1.location.x = c2.rect.left - c1.rect.width
                    elif t1.velocity[0] < 0:
                        t1.velocity[0] = 0
                        t1.location.x = c2.rect.right
                    res = True
        return res
    
    def bind_transform(self, transform:HXtransform, sgrid) -> None:
        """ binds an object's location to the spatial grid it was created in"""
        if transform.location.x <= 0:
            transform.velocity.x = 0
            transform.location.x = 1
        elif transform.location.x >= sgrid.size.x-transform.size.x:
            transform.velocity.x = 0
            transform.location.x = sgrid.size.x-transform.size.x
        
        if transform.location.y <= 0:
            transform.velocity.y = 0
            transform.location.y = 1
        elif transform.location.y >= sgrid.size.y-transform.size.y:
            transform.velocity.y = 0
            transform.location.y = sgrid.size.y-transform.size.y

    def update(self, snodes, dt, *args, **kwargs) -> None:
        try:
            snode = snodes.pop()
            for obj in snode.objects:
                if obj == None: continue
                c = obj.get_component(HXcollider)
                t = obj.get_component(HXtransform)
                if not t or not c:continue
                
                self.gravity(obj, dt)
                t.location.y += t.velocity.y * dt
                c.update(t.location)
                self.aabby(obj, snode.objects)
                
                t.location.x += t.velocity.x * dt
                self.friction(obj, dt)
                c.update(t.location)
                self.aabbx(obj, snode.objects)
                
                self.bind_transform(transform=t, sgrid=obj.sgrid)
                c.update(t.location)

        except (AttributeError, IndexError) as err: pass# hxLogger.log(hxLogger.HLX_LOG_ERROR, f"HXphysics: {err}") # off grid query
# --------------------------- #
