from split import Split
from tkinter import messagebox


class SplitTextBuilder:
    def __init__(self, lines, use_star_count, use_subsplits, swap_star_and_level_symbol, star_count_in_front):
        self.lines = lines
        self.use_star_count                = use_star_count
        self.use_subsplits                 = use_subsplits
        self.swap_star_and_level_symbol    = swap_star_and_level_symbol
        self.star_count_in_front           = star_count_in_front

        self._splits                       = []
        self._last_level_name              = ''
        self._name_index                   = 0
        self._stars_index                  = 0
        self._star_count                   = 0
        self._expected_arguments           = 1

        self._error = False

        self.init_nums()
        self.parse_split_lines()

    def init_nums(self):
        if self.use_star_count:
            self._expected_arguments += 1

        if self.use_subsplits:
            self._expected_arguments += 1

        if self.use_star_count and self.use_subsplits:
            self._name_index = 1
            self._stars_index = 2

        if self.use_star_count and not self.use_subsplits:
            self._name_index = 0
            self._stars_index = 1

        if self.use_subsplits and not self.use_star_count:
            self._name_index = 1

    def parse_split_lines(self):
        for line in self.lines:
            if line != '':
                line_parts = [part.strip() for part in line.split('\t')]
                split = Split()

                if len(line_parts) != self._expected_arguments:
                    self._error = True
                    messagebox.showerror('Error', 'Incorrect number of arguments. Check your "use star count" or "use subsplits" setting.')
                    break

                if self.use_subsplits:
                    if line_parts[0] != '':
                        self._last_level_name = line_parts[0]

                    split.level_name = self._last_level_name

                split.name = line_parts[self._name_index]

                if self.use_star_count:
                    split.stars = self.read_star_count(line_parts)

                    if split.stars == -1:
                        self._error = True
                        messagebox.showerror('Error', f'A star count was invalid. It was: {line_parts[self._stars_index]}')
                        break

                self._splits.append(split)

    def read_star_count(self, line_parts):
        try:
            if line_parts[self._stars_index] != '':
                line_stars = int(line_parts[self._stars_index])
                self._star_count += line_stars
                return self._star_count

        except ValueError:
            return -1

    def get_text(self):
        if self._error:
            return ''

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
            else:
                parts.append(split.name)

            parts.append('\n')

        return "".join(parts)

    def get_formatted_star_count(self, split):
        if not self.swap_star_and_level_symbol:
            return f'({split.stars})'

        else:
            return f'[{split.stars}]'
