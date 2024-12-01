from datetime import date


def get_player_age(birthdate: date) -> int:
    now = date.today()

    TODAY = now.day
    MONTH = now.month
    YEAR = now.year

    if birthdate.month > MONTH:
        return YEAR - birthdate.year - 1
    elif birthdate.month == MONTH:
        if birthdate.day > TODAY:
            return YEAR - birthdate.year - 1
        else:
            return YEAR - birthdate.year
    else:
        return YEAR - birthdate.year