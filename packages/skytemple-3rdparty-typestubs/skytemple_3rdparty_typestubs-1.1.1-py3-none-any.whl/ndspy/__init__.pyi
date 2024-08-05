import enum
from typing import Any

class Processor(enum.Enum):
    ARM9: int
    ARM7: int

class WaveType(enum.IntEnum):
    PCM8: int
    PCM16: int
    ADPCM: int

class Alignment:
    LEFT: int
    RIGHT: int
    H_CENTER: int
    TOP: int
    BOTTOM: int
    V_CENTER: int
    CENTER: Any

def indexInNamedList(L, name): ...
def findInNamedList(L, name): ...
def setInNamedList(L, name, value) -> None: ...
