import random

from data import PLAYERS
from game_funcs import prepare_player_info

print("""
##################################################
##################################################
      
                    WHO ARE YA?

##################################################
##################################################
""")

s_player = random.choice([key for key in PLAYERS.keys()])
s_team_stats, s_num_stats = prepare_player_info(PLAYERS, s_player)

n_guesses = 8
results = []

for guess in range(n_guesses):
    g_player = input('¡Adivina el jugador!: ')
    if g_player not in PLAYERS.keys():
        g_player = input(
            '¡Fuera de juego! Ese jugador no está en el terreno de juego, prueba con otro: '
        )
    g_team_stats, g_num_stats = prepare_player_info(PLAYERS, g_player)

    if s_player == g_player:
        print(f"""
##################################################
##################################################
              
            ¡SÍ!, EL JUGADOR ERA {s_player.upper()}
            QUE PUTO GRANDE
              
##################################################
##################################################
""")
        n_guesses = 0
        break
    else:
        for s_stat, g_stat in zip(s_team_stats, g_team_stats):
            if s_stat == g_stat:
                results.append(f'{g_stat}: ✅')
            else:
                results.append(f'{g_stat}: ❌')

        for s_stat, g_stat in zip(s_num_stats, g_num_stats):
            if s_stat > g_stat:
                results.append(f'{g_stat}: ⬆️')
            if s_stat < g_stat:
                results.append(f'{g_stat}: ⬇️')
            elif s_stat == g_stat:
                results.append(f'{g_stat}: ✅')

        print(results)
        results = []
        if n_guesses > 1:
            n_guesses -= 1
        elif n_guesses == 0:
            print(f"""Perdiste rey
                  El jugador era {s_player}
                  """)
            break
