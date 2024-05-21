import csv

from pylatex import TikZ
from pylatex.utils import NoEscape

from card import Card


class Event(Card):
    def __init__(self, id, fluff, action_text, order, foreshadowing):
        super().__init__(id, fluff, action_text)

        self.order = order
        self.foreshadowing = foreshadowing

    @classmethod
    def temporarystrypointsstatement(cls) -> str:
        return {
            "remove": r"\removetemporarystorypointsnow",
            "add": r"\addtemporarystorypointsnow",
        }

    @classmethod
    def load_from_csv(cls):
        result = []

        with open("./cardsources/Events.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                result.append(
                    cls(
                        row["ID"],
                        row["Fluff"],
                        cls.create_action_string(row),
                        row["Reihenfolge"],
                        row["Foreshadowing"],
                    )
                )

        return sorted(result, key=lambda x: int(x.order))

    def create_event_front_text(self):
        return NoEscape(
            r"\node[anchor=north, minimum width = 6cm, minimum height = \baselineskip + 0.75cm, draw] (frontnamebox) at (border.north) {};"
        ) + NoEscape(
            r"\node[anchor=center, font=\Huge] at (frontnamebox.center) {Event \emoji{calendar}};"
        )

    def create_sprint_text(self):
        radius = "2cm"

        return (
            NoEscape(
                f"\\node[anchor=north, minimum width = 6cm, minimum height = 6cm] (iterationbox) at ($(frontnamebox.south) + (0cm, -0.75cm)$) {{}};"
            )
            + NoEscape(
                f"\\draw[arrows={{-Stealth[fill=white, length=8mm]}}, double, double distance = 3pt, line width = 1pt] ($(iterationbox.center) + ({radius}, 0cm)$) arc[start angle=0, delta angle = 355, x radius = {radius}, y radius = {radius}];"
            )
            + NoEscape(
                f"\\node[anchor=center, font=\\fontsize{{80}}{{80}}\\selectfont] at (iterationbox.center) {{{self.order}}};"
            )
            + NoEscape(
                f"\\node[anchor=center, fill=white, text=black, font=\\Large] at ($(iterationbox.center) + (-{radius}, 0cm) + (0.3cm, 0cm)$) {{Iteration}};"
            )
        )

    def create_foreshadowing_text(self):
        return NoEscape(
            f"\\node[anchor=south, minimum width = 6cm, text width = 5cm, font=\\Large, text centered] at ($(border.south) + (0cm, 0.5cm)$) {{\\textit{{{self.foreshadowing}}}}};"
        )

    def create_color_indicator(self):
        return NoEscape(
            r"\node[anchor=north west, minimum width = 6cm, minimum height = 0.75cm, draw, fill=\eventcolor] at (frontnamebox.south west) {};"
        )

    def create_fluff_text(self):
        return NoEscape(
            f"\\node[anchor=north, text width=5cm] at ($(frontnamebox.south) + (0cm, -0.8cm)$) {{\\textit{{{self.fluff}}}}};"
        )

    def create_action_text(self):
        return NoEscape(
            f"\\node[anchor=south, text width=2in] at ($(border.south) + (0cm, 0.5cm)$) {{{self.action_text}}};"
        )

    def tikz_front(self, debug=False):
        tikz = TikZ()

        tikz.append(self.create_border())
        tikz.append(self.create_event_front_text())
        tikz.append(self.create_color_indicator())
        tikz.append(self.create_sprint_text())
        tikz.append(self.create_foreshadowing_text())

        if debug:
            tikz.append(self.create_debug_id())

        return tikz

    def tikz_back(self):
        tikz = TikZ()

        tikz.append(self.create_border())
        tikz.append(self.create_event_front_text())
        tikz.append(self.create_color_indicator())

        tikz.append(self.create_fluff_text())
        tikz.append(self.create_action_text())

        return tikz
