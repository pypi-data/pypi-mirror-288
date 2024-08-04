from .defines import *

import moderngl as mgl

# ------------------------------------------------------------ #
class HXwindow:
    def __init__(self, size:list[int]=[800, 600], title:str="Helix Window", color:list[int]=[50,50,50]) -> None:
        self.active:bool=False
        self.window_color:list[int]=color
        self.display_color:list[int]=[color[0]/2, color[1]/2, color[2]/2]
        self.display:pg.Surface=create_surface([400,300], color)
        self.internal:pg.Surface=create_window(size, title, flags=0)
        self.dimensions:np.ndarray=np.array(size, dtype=np.uint32)

    def getActive(self) -> bool: return self.active
    
    def activate(self) -> bool: self.active = True; return self.active

    def deactivate(self) -> bool: self.active = False; return self.active

    def free(self) -> None:
        self.display=None
        self.internal=None
        self.dimensions=None
        pg.display.quit()
# ------------------------------------------------------------ #

# ------------------------------------------------------------ #
def show_mouse() -> None:
    pg.mouse.set_visible(True)

def hide_mouse() -> None:
    pg.mouse.set_visible(False)

def create_window(win_size:list=[800, 600], title:str="Helix Window", flags=None) -> pg.Surface :
    win:pg.Surface = pg.display.set_mode(win_size)
    pg.display.set_caption(title)
    pg.display.set_icon(load_image(f"{HXASSET_DIR}helix-pride.png"))
    return win

def create_surface(size:list[int], color:list[int]) -> pg.Surface :
    s:pg.Surface = pg.Surface(size)
    s.fill(color)
    return s

def create_rect(location:list, size:list) -> pg.Rect :
    return pg.Rect(location, size)

def flip_surface(surface:pg.Surface, x:bool, y:bool) -> pg.Surface:
    return pg.transform.flip(surface, x, y)

def fill_surface(surface:pg.Surface, color:list[int]) -> None:
    surface.fill(color)

def natural_key(string_) -> list[int] :
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def draw_line(display:pg.Surface, color:list[int], start:list[int|float], end:list[int|float], width:int=1) -> None :
    pg.draw.line(display, color, start, end, width=width)
    
def draw_rect(display:pg.Surface, size:list[int], location:list[int|float], color:list[int]=[255,0,0], width:int=1) -> None :
    pg.draw.rect(display, color, pg.Rect(location, size), width=width)

def draw_circle(surface, color, center, radius, width=0):
    """
    Draw a circle on the given surface.
    
    :param surface: Pygame surface to draw on
    :param color: Color of the circle (tuple or list)
    :param center: Center of the circle (x, y) in screen coordinates
    :param radius: Radius of the circle
    :param width: Width of the circle outline. 0 means filled circle.
    """
    pg.draw.circle(surface, color, (int(center.x), int(center.y)), radius, width)

def rotate_surface(surface:pg.Surface, angle:float) -> None :
    return pg.transform.rotate(surface, angle)

def scale_surface(surface:pg.Surface, scale:list) -> pg.Surface :
    return pg.transform.scale(surface, scale)

def load_image(file_path:str) -> pg.Surface :
    image:pg.Surface = pg.image.load(file_path).convert_alpha()
    return image

def load_image_dir(dir_path:str) -> list[pg.Surface] :
    images:list = []
    for _, __, images in os.walk(dir_path):
        sorted_images = sorted(images, key=natural_key)
        for image in sorted_images:
            full_path = dir_path + '/' + image
            image_surface = load_image(full_path)
            images.append(image_surface)
            
def load_image_sheet(sheet_path:str, frame_size:list[int]) -> list[pg.Surface] :
    sheet = load_image(sheet_path)
    frame_x = int(sheet.get_size()[0] / frame_size[0])
    frame_y = int(sheet.get_size()[1] / frame_size[1])
    
    frames = []
    for row in range(frame_y):
        for col in range(frame_x):
            x = col * frame_size[0]
            y = row * frame_size[1]
            frame = pg.Surface(frame_size, pg.SRCALPHA).convert_alpha()
            frame.blit(sheet, (0,0), pg.Rect((x, y), frame_size))   # blit the sheet at the desired coords (texture mapping)
            frames.append(frame)
    return frames
# ------------------------------------------------------------ #    

