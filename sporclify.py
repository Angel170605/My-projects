with open ('./input.txt') as r, open('./lyrics.txt', 'w') as w:

    splitted = r.read().strip().split(' ')

    for _ in splitted:
        w.write(f'{_}\n')