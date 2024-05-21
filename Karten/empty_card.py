from pylatex import TikZ, TikZCoordinate, TikZNode

from card import Card


class EmptyCard(Card):
    def __init__(self):
        super().__init__("", "", "")

    def tikz_front(self, debug=False):
        tikz = TikZ()

        tikz.append(self.create_border())

        return tikz

    def tikz_back(self):
        return self.tikz_front()
