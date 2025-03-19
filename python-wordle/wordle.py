from data import word_list
from match_messages import *
from wordle_funcs import *

print(start_message)

start = str(input('¿Qué quieres hacer?: '))

if start == '1':
    print(instructions)
    start = str(input('¿Qué quieres hacer?: '))
if start == '2':
    exit()

secret_word = SetSecretWord(word_list)
guesses_left = 6

for _ in range(guesses_left):

    splitted_secret_word = InspectWord(secret_word)

    try_word = input('Intenta adivinar la palabra secreta: ').lower()
    if not IsValidWord(try_word):
        try_word = input(invalid_guess_word_message)

    if try_word == 'exit':
        break

    elif try_word == secret_word:
        print(win_message)
        break

    else:
        coincidences, emojis = CheckGuess(try_word, secret_word, splitted_secret_word)
        guesses_left -= 1
        ShowMatchInfo(coincidences, emojis, guesses_left)

    if guesses_left <= 0:
        print(lose_message)
        print(f'PD: La palabra era: {secret_word}')
