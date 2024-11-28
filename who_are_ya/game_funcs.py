from datetime import datetime


def get_payer_age(birth: str) -> int:
    now = datetime.now()

    TODAY = now.day
    MONTH = now.month
    YEAR = now.year

    birthday, birthmonth, birthyear = (int(date) for date in birth.split('-'))

    if birthmonth > MONTH:
        return YEAR - birthyear - 1
    elif birthmonth == MONTH:
        if birthday > TODAY:
            return YEAR - birthyear - 1
        else:
            return YEAR - birthyear
    else:
        return YEAR - birthyear


def prepare_player_info(PLAYERS: dict, player: str):
    nation, league, team, pos, birth, dorsal = PLAYERS[player]
    team_stats = [nation, league, team, pos]
    num_stats = [get_payer_age(birth), int(dorsal)]
    return team_stats, num_stats
