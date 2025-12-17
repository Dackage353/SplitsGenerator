from common.split_text_builder import SplitTextBuilder
from pathlib import Path


INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'
USE_SUBSPLITS = True
USE_STAR_COUNTS = True
SWAP_STAR_AND_LEVEL_SYMBOL = False
STAR_COUNT_IN_FRONT = False


if __name__ == '__main__':
    input = Path(INPUT_FILE_NAME)
    lines = input.read_text().splitlines()

    formatted_text = SplitTextBuilder.get_formatted_text(lines, USE_SUBSPLITS, USE_STAR_COUNTS, SWAP_STAR_AND_LEVEL_SYMBOL, STAR_COUNT_IN_FRONT)

    output = Path(OUTPUT_FILE_NAME)
    output.write_text(formatted_text)
    print('The splits have been generated. Look for output.txt')