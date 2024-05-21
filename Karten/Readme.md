This part deals with the playing cards for Extreme Pro-gaming. It is structures as follows:

- **cardsources**: descriptions of the cards, which are then converted to tex and pdfs.
- **output**: the generated cards will appear here as `card.pdfs` and `cards.tex`.
- **texsources**: tex commands for the effects of cards. We put this here in order to have the effects use a uniform language.
- **generate_card_pdf.py**: the main file to run

## Installation

After cloning the repository, simply create a virtual environment and install the required packages. After activating the virtual environment, you are ready to go.

```sh
# creating the virtual environment
python3 -m venv ./venv

# activating it
source venv/bin/activate

# installing requirements
python3 install -r requirements.txt
```

## Adapting the Cards

If you want to adapt the different values and fluff text of the cards, have a look at the files in the `cardsources` directory. 

If you want to adapt the effects, have a look at `texsources/effects.sty`. 

If you want to change the card design, have a look at the files `card.py` for general design elements such as the effect texts, `event_card.py` for the design of the effect cards, and `ticket_card.py` for the bug and feature cards.

## Generating the Cards

To generate the cards, simply run the generate_card_pdf script:

```sh
python3 generate_card_pdf.py
```

For adaptions from playtests, it can be useful to match the printed cards back to their digital versions. To make this easier, I added the `--debug` flag. If set, each card will get an ID that is also set in the card sources file.

```sh
python3 generate_card_pdf.py --debug
```

The cards will then be generated into the `output` directory.

To make the build process a bit easier in vscode, we added a launch configuration.  

## Printing the Cards

The cards are designed for DIN A4 paper. With that, simply print the cards with a duplex on the long edge. Afterward, the cards only need to be cut to size. Depending on the printer, the lines on the front and back might notch match perfectly.