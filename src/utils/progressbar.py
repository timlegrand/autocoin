import sys


class Progressbar():

    def __init__(self, size=15, msg='Downloading'):
        self.progress_length = 0
        self.size = size
        self.msg = msg

    def progress(self, progress_percents, msg=''):
        if self.progress_length:
            sys.stdout.write(self.progress_length*'\b')
        if not msg:
            msg = self.msg
        
        current_char = '-'
        if progress_percents < 100 and progress_percents > 0:
            current_char = '>'
        elif progress_percents == 100:
            current_char = '='
        progress_char_number = progress_percents * self.size // 100
        remaining_char_number = self.size - progress_char_number
        new_line = '\n' if progress_percents == 100 else ''
        if msg: msg += ' '
        progress_line = '{:30} [{}{}{}] {}%'.format(
            msg,
            progress_char_number*'=',
            current_char,
            remaining_char_number*'-',
            str(progress_percents))
        self.progress_length = len(progress_line)
        sys.stdout.write(progress_line + new_line)
        sys.stdout.flush()


if __name__ == '__main__':
    import progressbar
    p = Progressbar(size=15, msg='Testing #1 in progress')
    p.progress(0)
    print()
    p.progress(1)
    print()
    p.progress(19)
    print()
    p.progress(20)
    print()
    p.progress(99)
    print()
    p.progress(100)
    print()
    import time
    p.progress(0, msg='Testing #2 in progress')
    time.sleep(1)
    for i in range(0, 101):
        p.erase()
        p.progress(i, msg='Testing #2 in progress')
        time.sleep(0.03)