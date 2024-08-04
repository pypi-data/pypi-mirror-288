import os, sys
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = str(True)
import pygame as pg, numpy as np, moderngl as mgl, glm, glfw
import re, random, time, datetime, ctypes

HXASSET_DIR = __file__.removesuffix("defines.py")+"assets\\"

def set_text_attr(color):
    if sys.platform == "win32":
        console_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32. SetConsoleTextAttribute(console_handle, color)
    else:
        if color == 7:
            print("\u001b[0m", end = "", flush = True)

        elif color == 13:
            print("\u001b[31;1m", end = "", flush = True)

        elif color == 12:
            print("\u001b[31m", end = "", flush = True)

        else:
            ...

class HXlogger:
    DUMP_AT:int=8

    HLX_LOG_NONE:int=-1
    HLX_LOG_INFO:int=0
    HLX_LOG_WARNING:int=1
    HLX_LOG_ERROR:int=2
    HLX_LOG_FATAL:int=3
    HLX_LOG_SYSTEM:int=4

    def __init__(self):
        self.dumptime:float=0.0
        """ time since last dump """

        self.dump:bool=False
        """ flag to control when the logger dumps logs to the stdout """
        
        self.text = ""
        self.info_level = {
            self.HLX_LOG_INFO: "INFO",
            self.HLX_LOG_WARNING: "WARNING",
            self.HLX_LOG_ERROR: "ERROR",
            self.HLX_LOG_FATAL: "FATAL",
            self.HLX_LOG_SYSTEM: "SYSTEM"
        }
        self.info_color = {
            self.HLX_LOG_INFO: 3,
            self.HLX_LOG_WARNING: 6,
            self.HLX_LOG_ERROR: 1,
            self.HLX_LOG_FATAL: 0,
            self.HLX_LOG_SYSTEM: 10
        }

    def log(self, level, msg):
        stamp =  datetime.datetime.now().strftime("[%m/%d/%Y-%H:%M:%S]")
        self.text += datetime.datetime.now().strftime("[%m/%d/%Y-%H:%M:%S]") + f": Helix: %s: %s" % ({self.HLX_LOG_INFO: "info", self.HLX_LOG_WARNING: "warning", self.HLX_LOG_ERROR: "error", self.HLX_LOG_FATAL: "fatal error", self.HLX_LOG_SYSTEM: "system info"}[level], msg) + "\n"
        
        if level > self.HLX_LOG_NONE: #and self.dump:
            set_text_attr(5)
            print(f"{stamp} ", end = "", flush = True)
            set_text_attr(7)
            print("Helix: ", end = "", flush = True)
            set_text_attr(self.info_color[level])
            print("%s: " % self.info_level[level], end = "", flush = True)
            set_text_attr(self.info_color[level])
            print(f"{msg}\n")
            set_text_attr(7)
    
    def fixedLog(self, level, msg):
        stamp =  datetime.datetime.now().strftime("[%m/%d/%Y-%H:%M:%S]")
        self.text += datetime.datetime.now().strftime("[%m/%d/%Y-%H:%M:%S]") + f": Helix: %s: %s" % ({self.HLX_LOG_INFO: "info", self.HLX_LOG_WARNING: "warning", self.HLX_LOG_ERROR: "error", self.HLX_LOG_FATAL: "fatal error", self.HLX_LOG_SYSTEM: "system info"}[level], msg) + "\n"
        
        if level > self.HLX_LOG_NONE and self.dump:
            set_text_attr(5)
            print(f"FIXED LOG :: {stamp} ", end = "", flush = True)
            set_text_attr(7)
            print("Helix: ", end = "", flush = True)
            set_text_attr(self.info_color[level])
            print("%s: " % self.info_level[level], end = "", flush = True)
            set_text_attr(self.info_color[level])
            print(f"{msg}\n")
            set_text_attr(7)

    def get(self):
        return self.text

    def save(self, filePath):
        with open(filePath, "w") as file:
            file.write(self.text)

    def update(self, dt:float) -> None:
        if int(self.dumptime) == self.DUMP_AT:
            self.dump = True
            self.dumptime = 0.0
        else: 
            self.dump = False
            self.dumptime+=dt
hxLogger = HXlogger()

class Keyboard:
    # Letter keys
    A = pg.K_a
    B = pg.K_b
    C = pg.K_c
    D = pg.K_d
    E = pg.K_e
    F = pg.K_f
    G = pg.K_g
    H = pg.K_h
    I = pg.K_i
    J = pg.K_j
    K = pg.K_k
    L = pg.K_l
    M = pg.K_m
    N = pg.K_n
    O = pg.K_o
    P = pg.K_p
    Q = pg.K_q
    R = pg.K_r
    S = pg.K_s
    T = pg.K_t
    U = pg.K_u
    V = pg.K_v
    W = pg.K_w
    X = pg.K_x
    Y = pg.K_y
    Z = pg.K_z

    # Number keys
    Num0 = pg.K_0
    Num1 = pg.K_1
    Num2 = pg.K_2
    Num3 = pg.K_3
    Num4 = pg.K_4
    Num5 = pg.K_5
    Num6 = pg.K_6
    Num7 = pg.K_7
    Num8 = pg.K_8
    Num9 = pg.K_9

    # Function keys
    F1 = pg.K_F1
    F2 = pg.K_F2
    F3 = pg.K_F3
    F4 = pg.K_F4
    F5 = pg.K_F5
    F6 = pg.K_F6
    F7 = pg.K_F7
    F8 = pg.K_F8
    F9 = pg.K_F9
    F10 = pg.K_F10
    F11 = pg.K_F11
    F12 = pg.K_F12

    # Special keys
    Space = pg.K_SPACE
    Escape = pg.K_ESCAPE
    Enter = pg.K_RETURN
    Tab = pg.K_TAB
    Shift = pg.K_LSHIFT  # Left Shift
    Ctrl = pg.K_LCTRL    # Left Control
    Alt = pg.K_LALT      # Left Alt
    RShift = pg.K_RSHIFT  # Right Shift
    RCtrl = pg.K_RCTRL    # Right Control
    RAlt = pg.K_RALT      # Right Alt

    # Arrow keys
    Up = pg.K_UP
    Down = pg.K_DOWN
    Left = pg.K_LEFT
    Right = pg.K_RIGHT

    # Numpad keys
    NumPad0 = pg.K_KP0
    NumPad1 = pg.K_KP1
    NumPad2 = pg.K_KP2
    NumPad3 = pg.K_KP3
    NumPad4 = pg.K_KP4
    NumPad5 = pg.K_KP5
    NumPad6 = pg.K_KP6
    NumPad7 = pg.K_KP7
    NumPad8 = pg.K_KP8
    NumPad9 = pg.K_KP9
    NumPadDivide = pg.K_KP_DIVIDE
    NumPadMultiply = pg.K_KP_MULTIPLY
    NumPadSubtract = pg.K_KP_MINUS
    NumPadAdd = pg.K_KP_PLUS
    NumPadEnter = pg.K_KP_ENTER
    NumPadDecimal = pg.K_KP_PERIOD

    # Modifier keys
    LShift = pg.K_LSHIFT
    RShift = pg.K_RSHIFT
    LCtrl = pg.K_LCTRL
    RCtrl = pg.K_RCTRL
    LAlt = pg.K_LALT
    RAlt = pg.K_RALT
    LMeta = pg.K_LMETA
    RMeta = pg.K_RMETA
    LSuper = pg.K_LSUPER  # Windows key for left
    RSuper = pg.K_RSUPER  # Windows key for right

    # Miscellaneous keys
    CapsLock = pg.K_CAPSLOCK
    NumLock = pg.K_NUMLOCK
    ScrollLock = pg.K_SCROLLOCK
    PrintScreen = pg.K_PRINT
    Pause = pg.K_PAUSE
    Insert = pg.K_INSERT
    Delete = pg.K_DELETE
    Home = pg.K_HOME
    End = pg.K_END
    PageUp = pg.K_PAGEUP
    PageDown = pg.K_PAGEDOWN

    # Symbol keys
    Grave = pg.K_BACKQUOTE  # `~
    Minus = pg.K_MINUS      # -_
    Equals = pg.K_EQUALS    # =+
    LeftBracket = pg.K_LEFTBRACKET   # [{
    RightBracket = pg.K_RIGHTBRACKET # ]}
    Backslash = pg.K_BACKSLASH       # \|
    Semicolon = pg.K_SEMICOLON       # ;:
    Quote = pg.K_QUOTE               # '"
    Comma = pg.K_COMMA               # ,<
    Period = pg.K_PERIOD             # .>
    Slash = pg.K_SLASH               # /?
    BackSpace = pg.K_BACKSPACE
    Tab = pg.K_TAB
    Enter = pg.K_RETURN
    Menu = pg.K_MENU

class Mouse:
    LeftClick = 1
    WheelClick = 2
    RightClick = 3
    WheelUp = 4
    WheelDown = 5

