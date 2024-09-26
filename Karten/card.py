from typing import Dict

from pylatex import NoEscape, TikZCoordinate, TikZNode


class Card:
    def __init__(self, id, fluff, action_text):
        self.id = id
        self.fluff = fluff
        self.action_text = action_text

    @classmethod
    def temporarystrypointsstatement(cls) -> Dict[str, str]:
        return {
            "remove": r"\removetemporarystorypoints",
            "add": r"\addtemporarystorypoints",
        }

    @classmethod
    def create_action_string(cls, row) -> NoEscape:
        result = ""

        temporary_storypoint = row["Temporäre Veränderung an Storypoints"]
        if temporary_storypoint != "":
            try:
                temporary_storypoint = int(temporary_storypoint)
                if temporary_storypoint < 0:
                    result += NoEscape(
                        cls.temporarystrypointsstatement()["remove"]
                        + f"{{{abs(temporary_storypoint)}}} "
                    )
                elif temporary_storypoint > 0:
                    result += NoEscape(
                        cls.temporarystrypointsstatement()["add"]
                        + f"{{{temporary_storypoint}}} "
                    )
            except:
                pass

        permanent_storypoint = row["Permanente Veränderung an Storypoints"]
        if permanent_storypoint != "":
            try:
                permanent_storypoint = int(permanent_storypoint)
                if permanent_storypoint < 0:
                    result += NoEscape(
                        f"\\removepermanentstorypoints{{{abs(permanent_storypoint)}}} "
                    )
                elif permanent_storypoint > 0:
                    result += NoEscape(
                        f"\\addpermanentstorypoints{{{permanent_storypoint}}} "
                    )
            except:
                pass

        change_bugs = row["Veränderung an Bugs"]
        if change_bugs != "":
            try:
                change_bugs = int(change_bugs)
                if change_bugs == 1:
                    result += NoEscape(r"\addbug\ ")
                elif change_bugs > 1:
                    result += NoEscape(f"\\addbugs{{{change_bugs}}} ")
                else:
                    ValueError("Change in Bugs must be greater than 0")
            except:
                pass

        change_features = row["Veränderung an Features"]
        if change_features != "":
            try:
                change_features = int(change_features)
                if change_features == 1:
                    result += NoEscape(r"\addfeature\ ")
                elif change_features > 1:
                    result += NoEscape(f"\\addfeatures{{{change_features}}} ")
                else:
                    ValueError("Change in Features must be greater than 0")
            except:
                pass

        debt_backend = row["Debt Backend"]
        if debt_backend != "":
            try:
                debt_backend = int(debt_backend)
                if debt_backend < 0:
                    result += NoEscape(f"\\removedebtbackend{{{abs(debt_backend)}}} ")
                elif debt_backend > 0:
                    result += NoEscape(f"\\adddebtbackend{{{debt_backend}}} ")
            except:
                pass

        debt_frontend = row["Debt Frontend"]
        if debt_frontend != "":
            try:
                debt_frontend = int(debt_frontend)
                if debt_frontend < 0:
                    result += NoEscape(f"\\removedebtfrontend{{{abs(debt_frontend)}}} ")
                elif debt_frontend > 0:
                    result += NoEscape(f"\\adddebtfrontend{{{debt_frontend}}} ")
            except:
                pass

        if row["Sonstiger Effekt"] != "":
            result += NoEscape(row["Sonstiger Effekt"] + " ")

        return result

    def tikz_front(self, debug=False):
        raise NotImplementedError("Subclass Responsibility")

    def tikz_back(self):
        raise NotImplementedError("Subclass Responsibility")

    def create_border(self):
        return TikZNode(
            handle="border",
            at=TikZCoordinate(0, 0),
            text="",
            options="draw, minimum height=9cm, minimum width=6cm",
        )

    def create_debug_id(self):
        return NoEscape(
            f"\\node[anchor=north] at ($(border.north) + (0cm, -2.25cm)$) {{ID: {self.id}}};"
        )
