from os.path import join as path_join
from os import environ, makedirs

import shelve

import pyxel as px
from constants import WHITE, BROWN, PURPLE, RED, PINK, SCORE_FILE


def static_init(cls):
    cls.init()
    return cls


@static_init
class ScoresHandler:

    score = 0
    hiscores = []
    is_new = False
    scores_file = ""

    @classmethod
    def init(cls):
        config_path = path_join(
            environ.get("APPDATA")  # Windows
            or environ.get("XDG_CONFIG_HOME")  # Linux/macos XDG spec.
            or path_join(environ.get("HOME"), ".config"),  # fallback
            "lastspacefighter",
        )
        makedirs(config_path, exist_ok=True)
        cls.scores_file = path_join(config_path, SCORE_FILE)
        cls.hiscores = cls.load()

    @classmethod
    def load(cls):
        with shelve.open(cls.scores_file) as s:
            try:
                return s["hiscores"]
            except KeyError:
                # Default high-scores
                return [1000, 2000, 3000, 4000, 5000]

    @classmethod
    def pr(cls):
        print(f"hiscores: {cls.hiscores}")
        print(f"score: {cls.score}")
        print(f"New hiscore : {cls.is_new}")

    @classmethod
    def save(cls):
        with shelve.open(cls.scores_file) as s:
            s["hiscores"] = cls.hiscores

    @classmethod
    def update(cls, score):
        cls.score = score
        if score > min(cls.hiscores):
            cls.is_new = True
            lower_score = min(cls.hiscores)
            cls.hiscores.remove(lower_score)
            cls.hiscores.append(score)
            cls.hiscores.sort()
        else:
            cls.is_new = False

    @classmethod
    def draw_txt(cls):
        txts = []
        txts.append("HIGH-SCORE")

        all_scores = []
        done = False
        for n, sc in enumerate(cls.hiscores):
            line = f"{5-n}- {str(sc).rjust(7)}"
            if cls.is_new and sc == cls.score and not done:
                line += " *NEW*"
                done = True
            all_scores.insert(0, line)
        txts.extend(all_scores)

        txts.append("YOUR SCORE")
        txts.append(f"{str(cls.score).rjust(10)}")
        print("\n".join(txts))

    @classmethod
    def draw(cls, pos, for_end=False):
        cw = 4  # caracter width
        lh = 6  # line height
        col_title_score = PINK if for_end else PURPLE
        posx = pos.x
        posy = pos.y

        px.text(posx, posy, "HIGH-SCORE", PURPLE)

        done = False
        for n, sc in enumerate(cls.hiscores):
            y = posy + (5 - n) * 6
            px.text(posx, y, f"{5-n}- ", BROWN)
            px.text(posx + 3 * cw, y, str(sc).rjust(7), WHITE)
            if cls.is_new and sc == cls.score and not done:
                px.text(posx + 10 * cw, y, " < NEW", RED)
                done = True
        posy += lh * 6

        px.text(posx, posy, "LAST SCORE", col_title_score)
        posy += lh

        px.text(posx, posy, str(cls.score).rjust(10), WHITE)
