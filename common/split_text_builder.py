from common.data_classes import Split
from dataclasses import dataclass, field
from typing import List
from typing import Optional


@dataclass
class SplitTextBuilder:
    use_subsplits: bool = False
    use_star_count: bool = False
    swap_star_and_level_symbol: bool = False
    star_count_in_front: bool = False

    _splits: List[Split] = field(default_factory=list)

    _last_level_name: str = ''
    _name_index: Optional[int] = None
    _stars_index: Optional[int] = None
    _star_count: int = 0

    _lines: List[str] = field(default_factory=list)

    @staticmethod
    def get_formatted_text(lines, use_subsplits, use_star_count, swap_star_and_level_symbol, star_count_in_front):
        reader = SplitTextBuilder(
            _lines = lines,
            use_subsplits = use_subsplits,
            use_star_count = use_star_count,
            swap_star_and_level_symbol = swap_star_and_level_symbol,
            star_count_in_front = star_count_in_front
        )

        reader.parse_split_lines()
        return reader.splits_to_string()

    def reset_state(self):
        self._splits.clear()
        self._last_level_name = ''
        self._name_index = None
        self._stars_index = None
        self._star_count = 0

    def set_indexes(self):
        if self.use_subsplits:
            self._name_index = 1
            self._stars_index = 2

        else:                
            self._name_index = 0
            self._stars_index = 1

    def parse_split_lines(self):
        self.reset_state()
        self.set_indexes()

        for line in self._lines:
            line_parts = [part.strip() for part in line.split('\t')]
            split = Split()

            self.check_argument_count(line, len(line_parts))

            if self.use_subsplits:
                if line_parts[0] != '':
                    self._last_level_name = line_parts[0]

                split.level_name = self._last_level_name
            
            split.name = line_parts[self._name_index]

            if self.use_star_count:
                split.stars = self.read_star_count(line_parts)

            self._splits.append(split)

    def check_argument_count(self, line, line_parts_length):
        expected_arguments = 1
        if self.use_subsplits:
            expected_arguments += 1
        
        if self.use_star_count:
            expected_arguments += 1
                
        if line_parts_length < expected_arguments:
            raise ValueError(f'expected {expected_arguments} arguments and got {line_parts_length}. line was {line}')
        
    def read_star_count(self, line_parts):
        try:
            if line_parts[self._stars_index] != '':
                line_stars = int(line_parts[self._stars_index])
                self._star_count += line_stars
                return self._star_count

        except ValueError:
            raise ValueError(f'Stars argument wasn\'t a valid integer: {line_parts[self._stars_index]}')

    def splits_to_string(self):
        parts = []

        for i, split in enumerate(self._splits):
            if self.use_subsplits:
                end_of_group = (i == len(self._splits) - 1) or (split.level_name != self._splits[i + 1].level_name)

                if end_of_group:
                    parts.append(f'{{{split.level_name}}}')
                else:
                    parts.append('-')

            if self.use_star_count:
                if self.star_count_in_front:
                    if split.stars:
                        parts.append(self.get_formatted_star_count(split))
                        parts.append(' ')

                    parts.append(split.name)
                else:
                    parts.append(split.name)

                    if split.stars:
                        parts.append(' ')
                        parts.append(self.get_formatted_star_count(split))

            parts.append('\n')
        
        return "".join(parts)
                
    def get_formatted_star_count(self, split):
        if not self.swap_star_and_level_symbol:
            return f'({split.stars})'
        
        else:
            return f'[{split.stars}]'
