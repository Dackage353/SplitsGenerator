from dataclasses import dataclass, field
from common.data_classes import Split
from typing import List


@dataclass
class SplitTextBuilder:
    _use_subsplits: bool = False
    _swap_star_and_level_symbol: bool = False
    _star_count_in_front: bool = False

    _splits: List[Split] = field(default_factory=list)
    _split: Split = None

    _last_level_name: str = ''
    _name_index: int = None
    _stars_index: int = None
    _star_count: int = 0

    _lines: List[str] = field(default_factory=list)
    _line_parts: List[str] = field(default_factory=list)

    _final_text: str = ''

    @staticmethod
    def get_formatted_text(lines, use_subsplits=False, swap_star_and_level_symbol=False, star_count_in_front=False):
        reader = SplitTextBuilder(
            _lines = lines,
            _use_subsplits = use_subsplits,
            _swap_star_and_level_symbol = swap_star_and_level_symbol,
            _star_count_in_front = star_count_in_front
        )

        reader.parse_split_lines()
        reader.splits_to_string()
        return reader._final_text

    def parse_split_lines(self):
        for line in self._lines:
            self._line_parts = [part.strip() for part in line.split('\t')]
            self._split = Split()

            if self._use_subsplits:
                if len(self._line_parts) < 3:
                    raise Exception(f'expected 3 arguments and got {len}. line was {line}')
                
                if self._line_parts[0] != '':
                    last_level_name = self._line_parts[0]

                self._split.level_name = last_level_name
                self._name_index = 1
                self._stars_index = 2
                
            else:
                if len(self._line_parts) < 2:
                    raise Exception(f'expected 2 arguments and got {len}. line was {line}')
                
                self._name_index = 0
                self._stars_index = 1
            
            self._split.name = self._line_parts[self._name_index]

            try:
                if self._line_parts[self._stars_index] != '':
                    line_stars = int(self._line_parts[self._stars_index])
                    self._star_count += line_stars
                    self._split.stars = self._star_count

            except ValueError:
                print(f'stars argument wasn\'t a valid interger. line was {line}')

            self._splits.append(self._split)

    def splits_to_string(self):
        for i, split in enumerate(self._splits):
            if self._use_subsplits:
                end_of_group = (i == len(self._splits) - 1) or (split.level_name != self._splits[i + 1].level_name)

                if end_of_group:
                    self._final_text += f'{{{split.level_name}}}'
                else:
                    self._final_text += '-'

            if self._star_count_in_front:
                if split.stars != -1:
                    self._final_text += self.get_formatted_star_count(split)
                    self._final_text += ' '

                self._final_text += split.name
            else:
                self._final_text += split.name

                if split.stars != -1:
                    self._final_text += ' '
                    self._final_text += self.get_formatted_star_count(split)

            self._final_text += '\n'
                
    def get_formatted_star_count(self, split):
        if not self._swap_star_and_level_symbol:
            return f'({split.stars})'
        
        else:
            return f'[{split.stars}]'
