from hearthbreaker.effects.minion import Buff, IncreaseArmor, GiveCharge
import hearthbreaker.targeting
from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY
from hearthbreaker.game_objects import MinionCard, Minion, WeaponCard, Weapon


class ArathiWeaponsmith(MinionCard):
    def __init__(self):
        super().__init__("Arathi Weaponsmith", 4, CHARACTER_CLASS.WARRIOR, CARD_RARITY.COMMON)

    def create_minion(self, player):
        class BattleAxe(WeaponCard):
            def __init__(self):
                super().__init__("Battle Axe", 1, CHARACTER_CLASS.WARRIOR, CARD_RARITY.SPECIAL)

            def create_weapon(self, player):
                return Weapon(2, 2)

        def equip_battle_axe(minion):
            battle_axe = BattleAxe().create_weapon(player)
            battle_axe.equip(player)

        return Minion(3, 3, battlecry=equip_battle_axe)


class Armorsmith(MinionCard):
    def __init__(self):
        super().__init__("Armorsmith", 2, CHARACTER_CLASS.WARRIOR, CARD_RARITY.RARE)

    def create_minion(self, player):
        return Minion(1, 4, effects=[IncreaseArmor("damaged", 1, "minion", players="friendly", include_self=True)])


class CruelTaskmaster(MinionCard):
    def __init__(self):
        super().__init__("Cruel Taskmaster", 2, CHARACTER_CLASS.WARRIOR, CARD_RARITY.COMMON,
                         targeting_func=hearthbreaker.targeting.find_minion_battlecry_target)

    def create_minion(self, player):
        def deal_one_damage_and_give_two_attack(minion):
            if minion.card.target is not None:
                minion.card.target.damage(1, self)
                minion.card.target.change_attack(2)

        return Minion(2, 2, battlecry=deal_one_damage_and_give_two_attack)


class FrothingBerserker(MinionCard):
    def __init__(self):
        super().__init__("Frothing Berserker", 3, CHARACTER_CLASS.WARRIOR, CARD_RARITY.RARE)

    def create_minion(self, player):
        minion = Minion(2, 4, effects=[Buff("damaged", "minion", "self", 1, 0, "both", True)])
        return minion


class GrommashHellscream(MinionCard):
    def __init__(self):
        super().__init__("Grommash Hellscream", 8, CHARACTER_CLASS.WARRIOR, CARD_RARITY.LEGENDARY)

    def create_minion(self, player):
        return Minion(4, 9, charge=True, effects=[Buff("enraged", attack=6)])


class KorkronElite(MinionCard):
    def __init__(self):
        super().__init__("Kor'kron Elite", 4, CHARACTER_CLASS.WARRIOR, CARD_RARITY.COMMON)

    def create_minion(self, player):
        return Minion(4, 3, charge=True)


class WarsongCommander(MinionCard):
    def __init__(self):
        super().__init__("Warsong Commander", 3, CHARACTER_CLASS.WARRIOR, CARD_RARITY.FREE)

    def create_minion(self, player):
        return Minion(2, 3, effects=[GiveCharge("placed", "attack_less_than_or_equal_to_3", "other")])
