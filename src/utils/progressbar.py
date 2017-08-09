import sys

progress_length = 100


def print(progress_percents, size=100):
    global progress_length
    last_progress_char = '>' if progress_percents < 100 else '='
    progress_char_number = (progress_percents - 1) * size // 100
    remaining_char_number = (100 - progress_percents) * size // 100
    new_line = '\n' if progress_percents == 100 else ''
    progress_line = '[' + progress_char_number*'=' + last_progress_char + remaining_char_number*'-' + '] ' + str(progress_percents) + '%'
    progress_length = len(progress_line)
    sys.stdout.write(progress_line + new_line)
    sys.stdout.flush()


def erase():
    sys.stdout.write(progress_length*'\b')
