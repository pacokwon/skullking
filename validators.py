from skullconstants import HEADER_SIZE, SkullEnum


def choose_validator(payload, chosen):
    """
    Validator function for choose function in Player class

    params:
        payload: payload containing the information this validator function needs
        chosen: chosen value
    returns:
        True if chosen value is valid
        False otherwise
    """
    _has_theme = has_theme(payload["cards"], payload["theme"])
    special_tuple = (
        SkullEnum.WHITE,
        SkullEnum.MERMAID,
        SkullEnum.PIRATE,
        SkullEnum.GREENPIRATE,
        SkullEnum.SKULLKING,
    )

    if not chosen.isdecimal():
        print(f"Choose a number between 1 and {len(payload['cards'])}")
        return False
    if not (1 <= int(chosen) <= len(payload["cards"])):
        print(f"Choose a number between 1 and {len(payload['cards'])}")
        return False
    if (
        _has_theme
        and payload["cards"][int(chosen) - 1].CARDTYPE not in special_tuple
        and payload["cards"][int(chosen) - 1].CARDTYPE != payload["theme"]
    ):
        print(
            f"You have a card of the theme {payload['theme']}. You must choose that card"
        )
        return False

    return True


def yohoho_validator(payload, chosen):
    """
    Validator function for yohoho function in Player class

    params:
        payload: payload containing the information this validator function needs
        chosen: chosen value
    returns:
        True if chosen value is valid
        False otherwise
    """

    if not chosen.isdecimal():
        print(f"Choose a number!")
        return False

    return True


def has_theme(cards, theme):
    """
    evaluate if a set of cards has a specific theme
    params:
        cards: a list of SkullCard object
        theme: the desired theme to investigate on
    returns:
        True if there is a card of the given theme
        False otherwise
    """
    for card in cards:
        if card.CARDTYPE == theme:
            return True

    return False
