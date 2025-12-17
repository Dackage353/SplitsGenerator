from dataclasses import dataclass, field
from common.data_classes import Split
from typing import List


@dataclass
class SplitTextBuilder:
    use_subsplits: bool = False
    use_star_count: bool = False
    swap_star_and_level_symbol: bool = False
    star_count_in_front: bool = False

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
    def get_formatted_text(lines, use_subsplits, use_star_count, swap_star_and_level_symbol, star_count_in_front):
        reader = SplitTextBuilder(
            _lines = lines,
            use_subsplits = use_subsplits,
            use_star_count = use_star_count,
            swap_star_and_level_symbol = swap_star_and_level_symbol,
            star_count_in_front = star_count_in_front
        )

        reader.set_indexes()
        reader.parse_split_lines()
        reader.splits_to_string()
        return reader._final_text

    def parse_split_lines(self):
        for line in self._lines:
            self._line_parts = [part.strip() for part in line.split('\t')]
            self._split = Split()

            self.check_argument_count(line)

            if self.use_subsplits:
                if self._line_parts[0] != '':
                    self._last_level_name = self._line_parts[0]

                self._split.level_name = self._last_level_name
            
            self._split.name = self._line_parts[self._name_index]

            if self.use_star_count:
                self.read_star_count()

            self._splits.append(self._split)

    def set_indexes(self):
        if self.use_subsplits:
            self._name_index = 1
            self._stars_index = 2

        else:                
            self._name_index = 0
            self._stars_index = 1

    def read_star_count(self):
        try:
            if self._line_parts[self._stars_index] != '':
                line_stars = int(self._line_parts[self._stars_index])
                self._star_count += line_stars
                self._split.stars = self._star_count

        except ValueError:
            print(f'stars argument wasn\'t a valid interger. line was {line}')

    def check_argument_count(self, line):
        expected_arguments = 1
        if self.use_subsplits:
            expected_arguments += 1
        
        if self.use_star_count:
            expected_arguments += 1
                
        if len(self._line_parts) < expected_arguments:
            raise Exception(f'expected {expected_arguments} arguments and got {len(self._line_parts)}. line was {line}')

    def splits_to_string(self):
        for i, split in enumerate(self._splits):
            if self.use_subsplits:
                end_of_group = (i == len(self._splits) - 1) or (split.level_name != self._splits[i + 1].level_name)

                if end_of_group:
                    self._final_text += f'{{{split.level_name}}}'
                else:
                    self._final_text += '-'

            if self.star_count_in_front:
                if split.stars:
                    self._final_text += self.get_formatted_star_count(split)
                    self._final_text += ' '

                self._final_text += split.name
            else:
                self._final_text += split.name

                if split.stars:
                    self._final_text += ' '
                    self._final_text += self.get_formatted_star_count(split)

            self._final_text += '\n'
                
    def get_formatted_star_count(self, split):
        if not self.swap_star_and_level_symbol:
            return f'({split.stars})'
        
        else:
            return f'[{split.stars}]'
