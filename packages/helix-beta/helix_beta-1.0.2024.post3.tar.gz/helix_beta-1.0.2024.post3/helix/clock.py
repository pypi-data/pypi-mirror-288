from .defines import *

class HXclock:
    _internal = pg.time.Clock()
    
    def __init__(self, target:int=1000, fixed_step:float=1.0 / 60.0) -> None:
        self.target = target
        self.peak = 0
        self.average = 0
        self.current = 0
        self.total_fps = 0
        self.total_frames = 0
        self.up_time:float = 0.0
        self.delta_time:float = 0.0
        self.time:float = time.time()
        self.start_time:float = time.time()
        
        # flag to signal fixed updates
        self.fupdate:bool = False
        self.accumulator:float = 0.0
        self.fixed_step:float = fixed_step

    def get_ticks(self) -> int : return pg.time.get_ticks()

    def get_fupdate(self) -> bool :
        return self.accumulator >= self.fixed_step

    def reset_fupdate(self) -> None :
        self.accumulator -= self.fixed_step

    def tick(self) -> int :
        self.time:float = time.time()
        tick = self._internal.tick(self.target)
        self.delta_time = tick / 1000.0
        self.current = self._internal.get_fps()
        
        self.peak = max(self.peak, self.current)
        
        self.total_frames += 1
        self.total_fps += self.current
        
        self.average = self.total_fps / self.total_frames if self.total_frames > 0 else 0
        self.up_time += self.delta_time
        self.accumulator += self.delta_time
        if self.accumulator >= self.fixed_step : self.fupdate = True
        else: self.fupdate = False
        
        return tick


