from os import system, name

def clearScreen() -> None:
    """
    # func > clearScreen

    Clears screen, using the os module.
    It also handles the variation between the cls and clear command variation
    throughout systems!

    :returns: None
    """

    if name == "nt": system("cls")
    else: system("clear")

def clsScreen() -> None:
    """
    # func > clsScreen

    **Alias to clearScreen**
    :return: None
    """

    clearScreen()