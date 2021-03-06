import copy
import random
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
from neat.nn.nn_pure import create_ffphenotype as makenet
import pickle

class CustomAgent():

    net = None

    def __init__(self):
        super().__init__()
        winner = open('winner_chromosome', 'rb')
        chrome=pickle.load(winner)
        winner.close()
        self.net = makenet(chrome)

    def do_card_check(self, cards):
        return [True, True, True, True]

    def do_turn(self, player, game):
        def score(player):
            # get the inputs from the game and do net.sactivate(inputs)
            inputs = []
            inputs.append(max(player.hero.health/30.0,0))
            inputs.append(min((player.hero.base_attack+player.hero.temp_attack)/15, 1))
            inputs.append(player.mana/10)
            inputs.append(len(player.hand)/10)
            inputs.append(0)
            for minion in player.minions:
                inputs[4]+=(minion.base_attack+minion.temp_attack)/40
            inputs[4]=min(inputs[4], 1)
            inputs.append(max(player.opponent.hero.health/30,0))
            inputs.append(min((player.opponent.hero.base_attack+player.opponent.hero.temp_attack)/15, 1))
            inputs.append(len(player.opponent.hand)/10)
            inputs.append(0)
            for minion in player.opponent.minions:
                inputs[8]+=(minion.base_attack+minion.temp_attack)/40
            inputs[8]=min(inputs[8], 1)
            if player.opponent.hero.health<=0:
                inputs.append(1)
            else:
                inputs.append(0)
            return self.net.sactivate(inputs)[0]
        initial_player=player.copy(game)
        initial_opponent = player.opponent.copy(game)
        initial_player.opponent=initial_opponent
        initial_opponent.opponent=initial_player
        best_player=player.copy(game)
        best_opponent = player.opponent.copy(game)
        best_player.opponent=best_opponent
        best_opponent.opponent=best_player
        best_score = 0
        for x in range (0, 1000):
            while True:
                attack_minions = [minion for minion in filter(lambda minion: minion.can_attack(), player.minions)]
                if player.hero.can_attack():
                    attack_minions.append(player.hero)
                playable_cards = [card for card in filter(lambda card: card.can_use(player, player.game), player.hand)]
                if player.hero.power.can_use():
                    possible_actions = len(attack_minions) + len(playable_cards) + 1
                else:
                    possible_actions = len(attack_minions) + len(playable_cards)
                if random.randint(0, 25)<1:
                    possible_actions=0;
                if possible_actions > 0:
                    action = random.randint(0, possible_actions - 1)
                    if player.hero.power.can_use() and action == possible_actions - 1:
                        player.hero.power.use()
                    elif action < len(attack_minions):
                        attack_minions[action].attack()
                    else:
                        player.game.play_card(playable_cards[action - len(attack_minions)])
                else:
                    player_score = score(player)
                    if best_score<player_score:
                        best_score = player_score
                        player.setPlayer(game,best_player)
                        player.opponent.setPlayer(game,best_opponent)
                    initial_player.setPlayer(game,player)
                    initial_opponent.setPlayer(game,player.opponent)
                    break
        
        best_player.setPlayer(game,player)
        best_opponent.setPlayer(game,player.opponent)
        return
		       

    def choose_target(self, targets):
        return targets[random.randint(0, len(targets) - 1)]

    def choose_index(self, card, player):
        return random.randint(0, len(player.minions))

    def choose_option(self, *options):
        return options[random.randint(0, len(options) - 1)]

class RandomAgent():
    def __init__(self):
        super().__init__()

    def do_card_check(self, cards):
        return [True, True, True, True]

    def do_turn(self, player, game):
        while True:
            attack_minions = [minion for minion in filter(lambda minion: minion.can_attack(), player.minions)]
            if player.hero.can_attack():
                attack_minions.append(player.hero)
            playable_cards = [card for card in filter(lambda card: card.can_use(player, player.game), player.hand)]
            if player.hero.power.can_use():
                possible_actions = len(attack_minions) + len(playable_cards) + 1
            else:
                possible_actions = len(attack_minions) + len(playable_cards)
            if possible_actions > 0:
                action = random.randint(0, possible_actions - 1)
                if player.hero.power.can_use() and action == possible_actions - 1:
                    player.hero.power.use()
                elif action < len(attack_minions):
                    attack_minions[action].attack()
                else:
                    player.game.play_card(playable_cards[action - len(attack_minions)])
            else:
                return    

    def choose_target(self, targets):
        return targets[random.randint(0, len(targets) - 1)]

    def choose_index(self, card, player):
        return random.randint(0, len(player.minions))

    def choose_option(self, *options):
        return options[random.randint(0, len(options) - 1)]
