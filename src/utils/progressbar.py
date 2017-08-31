import sys


class Progressbar():

    def __init__(self, size=15, msg='Downloading'):
        self.progress_length = 0
        self.size = size
        self.msg = msg
        self.complete = False

    def progress(self, progress=0, total=0, msg=''):
        if total:
            progress_percents = progress * 100 / total
        else:
            progress_percents = progress
        if self.progress_length:
            # sys.stdout.write(self.progress_length*'\b')
            print()
        if not msg:
            msg = self.msg
        else:
            self.msg = msg

        current_char = '-'
        if progress_percents < 100 and progress_percents > 0:
            current_char = '>'
        elif progress_percents == 100:
            current_char = '='
            self.complete = True
        progress_char_number = int(progress_percents * self.size // 100)
        remaining_char_number = self.size - progress_char_number
        new_line = '\n' if progress_percents == 100 else ''
        if msg:
            msg += ' '
        progress_line = '{:30} [{}{}{}] {:3<}%'.format(
            msg,
            progress_char_number*'=',
            current_char,
            remaining_char_number*'-',
            int(progress_percents))
        if total:
            progress_line += '  ({}/{})'.format(progress, total)
        self.progress_length = len(progress_line)
        sys.stdout.write(progress_line + new_line)
        sys.stdout.flush()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self.complete:
            sys.stdout.write('\n')
            sys.stdout.flush()


if __name__ == '__main__':
    p = Progressbar(size=15, msg='Testing #1 in progress...')
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
    p.progress(0, msg='Testing #2 in progress...')
    time.sleep(1)
    total = 200
    for i in range(0, total, 3):
        p.progress(i, total)
        time.sleep(0.03)

    print('Should write a new line soon...')
    time.sleep(1)
    with Progressbar() as p:
        pass
    print('End.')
