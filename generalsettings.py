FUNDO = "#0F180E"
COR_LETRAS = "#FFFFFF"
# COR_LETRAS = "#686464"
COR_BOTOES = "#051C03"
COR_BOTAO_BACKGROUND = "#03150C"
COR_BOTAO_FOREGROUND = "white"
FONTE = ("Helvetica", 12)
FONTE3 = ("Helvetica", 12, 'italic')
FONTE2 = ("Helvetica", 14, "italic")


def label():
    return {"font": FONTE, "background": FUNDO, "fg": COR_LETRAS}


def label_livros_info():
    return {"font": FONTE3, "background": FUNDO, "fg": COR_LETRAS}


def label_livros():
    return {"font": FONTE2, "background": FUNDO, "fg": COR_LETRAS}


def button():
    return {"font": FONTE, "background": COR_BOTOES,
            "fg": COR_LETRAS, "width": 15,
            "activebackground": COR_BOTAO_BACKGROUND, "activeforeground": COR_BOTAO_FOREGROUND}


def entry():
    return {"font": FONTE, "justify": "left", "background": "#202D20", "fg": "white", "insertbackground": "yellow"}


def frame():
    return {"background": FUNDO}


def labelframe():
    return {"background": COR_BOTOES}


def text():
    return {"background": '#424D42', "font": FONTE, "foreground": COR_LETRAS, "border": 2, "relief": "sunken",
            "insertbackground": "yellow"}


def checkbox():
    return {'background': FUNDO, 'activebackground': FUNDO, }


def radio():
    return {"background": FUNDO, "relief": "sunken", "fg": COR_LETRAS,
            'activebackground': '#202D20',  'activeforeground': COR_LETRAS, "font": FONTE, 'selectcolor': '#202D20'}
