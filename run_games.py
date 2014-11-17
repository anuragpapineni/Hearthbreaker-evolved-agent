from hearthbreaker.agents.basic_agents import *
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.game_objects import Game, card_lookup, Deck
from hearthbreaker.cards import *
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import timeit

config.load('evolve_agent_config')

# set node gene type
chromosome.node_gene_type = genome.NodeGene

def load_deck(filename):
    cards = []
    character_class = CHARACTER_CLASS.MAGE

    with open(filename, "r") as deck_file:
        contents = deck_file.read()
        items = contents.splitlines()
        for line in items[0:]:
            parts = line.split(" ", 1)
            count = int(parts[0])
            for i in range(0, count):
                card = card_lookup(parts[1])
                if card.character_class != CHARACTER_CLASS.ALL:
                    character_class = card.character_class
                cards.append(card)

    if len(cards) > 30:
        pass

    return Deck(cards, character_class)


def do_stuff(net):
    def play_game():
        new_game = game.copy()
        new_game.start()
    deck1 = load_deck("example.hsdeck")
    deck2 = load_deck("example.hsdeck")
    game = Game([deck1, deck2], [CustomAgent(net), RandomAgent()])
    game.start()

    print(timeit.timeit(play_game, 'gc.enable()', number=1000))

if __name__ == "__main__":
    net = None
    do_stuff(net)
