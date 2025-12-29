from dataclasses import dataclass
from typing import Optional


@dataclass
class Split:
    level_name: str = ''
    name: str = ''
    stars: Optional[int] = None
