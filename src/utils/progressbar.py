import sys


progress_length = 100


def update(progress_percents, size=15, msg=''):
    global progress_length
    current_char = '-'
    if progress_percents < 100 and progress_percents > 0:
        current_char = '>'
    elif progress_percents == 100:
        current_char = '='
    progress_char_number = progress_percents * size // 100
    remaining_char_number = size - progress_char_number
    new_line = '\n' if progress_percents == 100 else ''
    if msg: msg += ' '
    progress_line = '{:25} [{}{}{}] {}%'.format(
        msg,
        progress_char_number*'=',
        current_char,
        remaining_char_number*'-',
        str(progress_percents))
    progress_length = len(progress_line)
    sys.stdout.write(progress_line + new_line)
    sys.stdout.flush()


def erase():
    sys.stdout.write(progress_length*'\b')
