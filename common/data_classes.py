from dataclasses import dataclass, field

@dataclass
class Split:
    level_name: str = ''
    name: str = ''
    stars: int = -1