import argparse

from pylatex import Center, Command, Document, NewLine, NewPage
from pylatex.utils import NoEscape

from empty_card import EmptyCard
from event_card import Event
from ticket_card import Bug, Feature

cards_per_row = 3
cards_per_page = 9


def add_cards_in_rows(main_container, cards_for_row):
    with main_container.create(Center()) as container:
        for row in cards_for_row:
            for card in row:
                container.append(card)
            container.append(NewLine())


def _split_cards_in_rows(cards, cards_per_row):
    return [cards[i : i + cards_per_row] for i in range(0, len(cards), cards_per_row)]


def _add_cards_front(main_container, cards, cards_per_row):
    cards_for_row = _split_cards_in_rows(cards, cards_per_row)
    add_cards_in_rows(main_container, cards_for_row)


def _add_cards_back(main_container, cards, cards_per_row):
    cards_for_row = _split_cards_in_rows(cards, cards_per_row)
    cards_for_row = [list(reversed(row)) for row in cards_for_row]
    add_cards_in_rows(main_container, cards_for_row)


def add_ticket_pages(
    main_container, tickets, cards_per_page, cards_per_row, debug=False
):
    tickets_for_page = [
        tickets[i : i + cards_per_page] for i in range(0, len(tickets), cards_per_page)
    ]

    last_page = tickets_for_page[-1]
    while len(last_page) % cards_per_row != 0:
        last_page.append(EmptyCard())

    for ticket_list in tickets_for_page:
        fronts = [ticket.tikz_front(debug) for ticket in ticket_list]
        backs = [ticket.tikz_back() for ticket in ticket_list]

        _add_cards_front(main_container, fronts, cards_per_row)
        main_container.append(NewPage())
        _add_cards_back(main_container, backs, cards_per_row)
        main_container.append(NewPage())


def create_document(debug: bool, babel_option: str, language: str):
    doc = Document(
        documentclass="scrartcl",
    )

    doc.preamble.append(Command("usepackage", "geometry"))
    doc.packages.append(Command("usepackage", "tabularx"))
    doc.packages.append(Command("usepackage", "graphicx"))
    doc.packages.append(Command("usepackage", "multirow"))
    doc.packages.append(Command("usepackage", "varwidth"))
    doc.packages.append(Command("usepackage", "tikz"))
    doc.packages.append(Command("usepackage", "babel", options=babel_option))
    doc.packages.append(Command("usepackage", "xcolor"))
    doc.packages.append(Command("usepackage", "mathabx"))
    doc.packages.append(Command("usepackage", "shapepar"))
    doc.packages.append(Command("usepackage", f"../../texsources/{language}/effects"))

    doc.preamble.append(
        NoEscape(r"\usetikzlibrary{positioning, calc, shapes, arrows.meta}")
    )
    doc.preamble.append(NoEscape(r"\pagenumbering{gobble}"))
    doc.preamble.append(
        NoEscape(r"\geometry{a4paper, top=0.5cm, left=14mm, right=14mm, bottom=0.5cm}")
    )

    doc.append(NoEscape(r"\setemojifont{TwemojiMozilla}"))

    add_ticket_pages(
        doc, Feature.load_from_csv(language), cards_per_page, cards_per_row, debug
    )
    add_ticket_pages(
        doc, Bug.load_from_csv(language), cards_per_page, cards_per_row, debug
    )
    add_ticket_pages(
        doc, Event.load_from_csv(language), cards_per_page, cards_per_row, debug
    )

    doc.generate_tex(f"output/{language}/cards")
    doc.generate_pdf(
        f"output/{language}/cards", clean=True, clean_tex=False, compiler="lualatex"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="If this flag is set, each card will get an ID printed on. This way it is easier to match the printed  cards from playtests to the digital versions.",
    )
    parser.add_argument(
        "--language",
        action="store",
        choices=["german", "english", "both"],
        default="german",
        const="german",
        nargs="?",
        required=False,
        help="Provide the language you want the cards to be in. Currently supported languages are german and english. Default is german.",
    )

    args = parser.parse_args()

    if args.language in ("german", "both"):
        create_document(args.debug, "ngerman", "german")

    if args.language in ("english", "both"):
        create_document(args.debug, "american", "english")
