Hearthbreaker-evolved-agent
===========================
Hiya! This is an agent which uses neuroevolution to create an AI for the Hearthstone simulator hearthbreaker. The AI reach 
surprisingly high levels of gameplay relatively fast. In order to play against an evolved agent you need Python3, as well
as neatPython installed and converted to Python3. For the most part this can be done by running 2to3 on the library.
The agent uses a constantly evolving neural network as a board evaluator to bmake its decisions. Things it considers
include total attack of enemy minions, total attack of player minions, total health of player minions, attack of player,
health of player, health of opponent, cards in player's hand, and the lethality status of the opponent.
