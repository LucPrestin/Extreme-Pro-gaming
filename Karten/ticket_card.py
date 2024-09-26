import csv

from pylatex import TikZ
from pylatex.utils import NoEscape

from card import Card


class Ticket(Card):
    def __init__(
        self, id, fluff, action_text, hint, cost, system_part, is_start_ticket, title
    ):
        super().__init__(id, fluff, action_text)

        self.is_start_ticket = is_start_ticket
        self.hint = hint
        self.cost = cost
        self.system_part = system_part
        self.title = title
    @classmethod
    def load_from_csv(cls, language: str):
        raise NotImplementedError("Subclass Responsibility")
        

    @classmethod
    def load_from_file(cls, filename):
        result = []

        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                result.append(
                    cls(
                        row["ID"],
                        row["Fluff"],
                        cls.create_action_string(row),
                        row["Effekthinweis"],
                        row["Kosten"],
                        row["Systemteil"],
                        row["Ist Start-Ticket"] == "Ja",
                        row["Titel"],
                    )
                )

        return sorted(result, key=lambda x: x.is_start_ticket, reverse=True)

    @property
    def system_part_color(self):
        if self.system_part == "Frontend":
            return r"\frontendcolor"
        elif self.system_part == "Backend":
            return r"\backendcolor"
        else:
            return "black"

    @property
    def frontnametext(self):
        raise NotImplementedError("Subclass responsibility")

    def create_ticket_kind_symbol_front(self):
        return NoEscape(
            f"\\node[anchor=north, minimum width = 6cm, minimum height = \\baselineskip + 0.75cm, draw] (frontnamebox) at (border.north) {{}};"
        ) + NoEscape(
            f"\\node[anchor=center, font=\\Huge] at (frontnamebox.center) {{{self.frontnametext}}};"
        )

    def create_ticket_kind_symbol_back(self):
        return self.create_ticket_kind_symbol_front()

    def create_system_part_symbol(self):
        anchor = "north west" if self.system_part == "Frontend" else "north east"
        position = (
            "(frontnamebox.south west)"
            if self.system_part == "Frontend"
            else "(frontnamebox.south east)"
        )

        return NoEscape(
            f"\\node[anchor={anchor}, fill={self.system_part_color}, draw, font=\\Large, minimum width=3cm, minimum height = 0.75cm] at {position} {{{self.system_part}}};"
        )

    def create_cost_symbol(self):
        costbox_height = "2.1cm"
 
        tikz_command = NoEscape(
            f"\\node[anchor=north, minimum width = 5cm, minimum height = {costbox_height}, draw, rounded corners] (costbox) at ($(frontnamebox.south) + (0cm, -2cm)$) {{}};"
        )
        tikz_command += NoEscape(
            f"\\node[anchor=west, minimum width = 2.5cm, minimum height = {costbox_height}] (costboxwest) at (costbox.west) {{}};"
        )
        tikz_command += NoEscape(
            f"\\node[anchor=east, minimum width = 2.5cm, minimum height = {costbox_height}] (costboxeast) at (costbox.east) {{}};"
        )
        tikz_command += NoEscape(
            f"\\node[anchor=west, fill=white, font=\\large] at ($(costbox.north west) + (0.25cm, 0cm)$) {{\\textkosten}};"
        )

        teddy_bear = lambda anchor, size="huge": NoEscape(
            f"\\node[anchor = {anchor}, font=\\{size}] at (costboxwest.center) {{\\emoji{{teddy-bear}}}};"
        )

        if self.cost == "1":
            tikz_command += teddy_bear("center", "Huge")
        elif self.cost == "2":
            tikz_command += teddy_bear("east", "Huge") + teddy_bear("west", "Huge")
        elif self.cost == "3":
            tikz_command += (
                teddy_bear("south")
                + teddy_bear("north west")
                + teddy_bear("north east")
            )

        tikz_command += NoEscape(
            r"\node[anchor=center, font=\Large] at (costbox.center) {+};"
        )

        tikz_command += NoEscape(
            r"\node[anchor = west, font=\Huge] at ($(costboxeast.west) + (0.25cm, 0cm)$) {1};"
        )
        tikz_command += NoEscape(
            r"\node[anchor=north west, font=\Large] at ($(costboxeast.north west) + (0.75cm, -0.4cm)$) {\emoji{teddy-bear}};"
        )
        tikz_command += NoEscape(
            f"\\node[anchor=north west, draw, circle, fill={self.system_part_color}, minimum size = 0.5cm] at ($(costboxeast.north west) + (1.5cm, -1.25cm)$) {{}};"
        )
        tikz_command += NoEscape(
            r"\draw ($(costboxeast.south west) + (0.9cm, 0.55cm)$) -- ($(costboxeast.north east) + (-0.6cm, -0.55cm)$);"
        )

        return NoEscape(tikz_command)

    def create_start_symbol(self):
        anchor = "north east" if self.system_part == "Frontend" else "north west"
        position = (
            "(frontnamebox.south east)"
            if self.system_part == "Frontend"
            else "(frontnamebox.south west)"
        )

        return NoEscape(
            f"\\node[anchor={anchor}, font=\\Large, minimum width=3cm] at {position} {{Start}};"
        )

    def create_effect_symbol(self):
        command = NoEscape(
            r"\node[anchor=center, draw, rounded corners, minimum width = 1.5cm, minimum height = 1.5cm] (effectbox) at ($(costbox.south) + (0cm, -1cm)$) {};"
        )

        if self.hint == "positive":
            command += NoEscape(
                f"\\node[anchor=center, single arrow, draw, fill=white, rotate=90, minimum height=1cm, minimum width=1cm] at (effectbox.center) {{}};"
            )
        elif self.hint == "negative":
            command += NoEscape(
                f"\\node[anchor=center, single arrow, draw, fill=white, rotate=270, minimum height=1cm, minimum width=1cm] at (effectbox.center) {{}};"
            )
        else:
            command += NoEscape(
                f"\\node[anchor=center, fill=white, font=\\fontsize{{30}}{{30}}\\selectfont] at (effectbox.center) {{?}};"
            )

        return command

    def create_title_text(self):
        return NoEscape(
            f"\\node[anchor=south, text width=5cm, font=\\large] at ($(border.south) + (0cm, 0.5cm)$) {{\\textit{{{self.title}}}}};"
        )

    def create_fluff_text(self):
        return NoEscape(
            f"\\node[anchor=north, text width=5cm] at ($(frontnamebox.south) + (0cm, -0.8cm)$) {{\\textit{{{self.fluff}}}}};"
        )

    def create_action_text(self):
        return NoEscape(
            f"\\node[anchor=south, text width=5cm] at ($(border.south) + (0cm, 0.5cm)$) {{{self.action_text}}};"
        )

    def tikz_front(self, debug=False):
        tikz = TikZ()

        tikz.append(self.create_border())

        tikz.append(self.create_ticket_kind_symbol_front())
        tikz.append(self.create_system_part_symbol())

        tikz.append(self.create_title_text())
        tikz.append(self.create_cost_symbol())
        tikz.append(self.create_effect_symbol())

        if self.is_start_ticket:
            tikz.append(self.create_start_symbol())

        if debug:
            tikz.append(self.create_debug_id())

        return tikz

    def tikz_back(self):
        tikz = TikZ()

        tikz.append(self.create_border())

        tikz.append(self.create_ticket_kind_symbol_back())
        tikz.append(self.create_system_part_symbol())
        tikz.append(self.create_fluff_text())
        tikz.append(self.create_action_text())

        return tikz


class Bug(Ticket):
    @classmethod
    def load_from_csv(cls, language: str):
        return super().load_from_file(f"./cardsources/{language}/Bugs.csv")

    @property
    def frontnametext(self):
        return r"\bug"


class Feature(Ticket):
    @classmethod
    def load_from_csv(cls, language: str):
        return super().load_from_file(f"./cardsources/{language}/Features.csv")

    @property
    def frontnametext(self):
        return r"\feature"
