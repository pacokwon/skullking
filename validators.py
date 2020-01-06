from skullconstants import HEADER_SIZE, SkullEnum


def choose_validator(obj, theme_of_table):
    _has_theme = obj.has_theme(theme_of_table)
    special_tuple = (
        SkullEnum.WHITE,
        SkullEnum.MERMAID,
        SkullEnum.PIRATE,
        SkullEnum.GREENPIRATE,
        SkullEnum.SKULLKING,
    )

    def validator(chosen):
        if not chosen.isdecimal():
            print(f"Choose a number between 1 and {len(obj.cards)}")
            return False
        if not (1 <= int(chosen) <= len(obj.cards)):
            print(f"Choose a number between 1 and {len(obj.cards)}")
            return False
        if (
            _has_theme
            and self.cards[int(chosen) - 1].CARDTYPE not in special_tuple
            and self.cards[int(chosen) - 1].CARDTYPE != theme_of_table
        ):
            print(
                f"You have a card of the theme {theme_of_table}. You must choose that card"
            )
            return False

        return True

    return validator


def yohoho_validator():
    def validator(chosen):
        if not chosen.isdecimal():
            print(f"Choose a number!")
            return False

        return True

    return validator

