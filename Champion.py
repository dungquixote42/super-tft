import numpy as np

from config import *


class Champion:
    def __init__(self, cdat, star, ability):
        # self.name = cdat["name"]
        self.traits = cdat["traits"]
        self.cost = cdat["cost"]
        self.hp_max = cdat["hp_max"]
        self.ad = cdat["ad"]
        self.atk_range = cdat["atk_range"]
        self.atk_spd_base = cdat["atk_spd_base"]
        self.armor = cdat["armor"]
        self.mr = cdat["mr"]
        self.mp_max = cdat["mp_max"]
        self.mp_start = cdat["mp_start"]
        self.star = star
        self._ability = ability
        if "attack" in cdat:
            self._attack = cdat["attack"]

        # default
        self.crit = 0.25

        # derived
        self.atk_spd = self.atk_spd_base
        self.is_melee = self.atk_range == 1

        # effects from abilities or items
        self.dmg_redux = 0.0

        # arena
        self.bench = None

        # other
        self.timers_ms = np.zeros(HANDLE_COUNT, dtype=np.uint16)
        self.reset()

    def _attack(self, allies, enemies):
        action = None
        # TODO: evaluate action
        if action:
            self.mp += 10
        return action

    def _ability(self, allies, enemies, bench):
        action = None
        # TODO: evaluate action
        if action:
            self.mp = min(self.mp - self.mp_max, self.mp_max)
            self.timers_ms[[CAST, MANALOCK]] = CAST_MS, MANALOCK_MS
            self.casting = True
        return action

    def _getset_ability_target(self):
        pass

    def _getset_attack_target(self):
        pass

    def add_to_deck(self):  # purchase, neeko, etc.
        self.board = np.zeros((7, 8, 8), dtype=np.uint16)
        self.xyz = np.ndarray(3, dtype=np.uint8)

    def apply_buff(self):
        pass

    def apply_damage(self, phy_dmg, mag_dmg, true_dmg):

        # handle armor, mr
        adj_phy_dmg = (phy_dmg - self.dmg_redux) * 100.0 / (100.0 + self.armor)
        adj_mag_dmg = (mag_dmg - self.dmg_redux) * 100.0 / (100.0 + self.mr)
        adj_dmg = adj_phy_dmg + adj_mag_dmg

        # handle hp, mp
        self.hp -= adj_dmg + true_dmg
        if self.hp > 0 and (self.timers_ms[MANALOCK] <= 0):
            self.mp += min(42.5, 0.01 * (phy_dmg + mag_dmg) + 0.03 * adj_dmg)

    def apply_debuff(self):
        pass

    def apply_heal(self, heal, heal_max, heal_missing):
        self.hp += (
            heal + (self.hp_max * heal_max) + (self.hp_max - self.hp) * heal_missing
        )

    def place_on_bench(self):
        pass

    def place_on_board(self, x, y, z):
        self.xyz[:] = [x, y, z]

    def item_add(self):
        pass

    def item_pop(self):
        pass

    def reset(self):  # right before next round
        self.hp = self.hp_max
        self.mp = self.mp_start
        self.attack_target = None

        # timers in milliseconds
        self.timers_ms[:] = 0

        # flags with timers
        self.moving = True
        self.windingup = False
        self.attacking = False
        self.casting = False
        self.channeling = False
        self.manalocked = False

        # flags without timers
        self.chase = False

    def tick(self, allies, enemies, bench):
        action = None

        # evaluate cc
        if ():
            pass

        # evaluate current action
        interruptible = False
        need_new_action = False
        if self.moving:
            self.moving = self.timers_ms[MOVE] > 0
            need_new_action = not self.moving
        elif self.windingup:
            self.windingup = self.timers_ms[WINDUP] > 0
            if not self.windingup:
                action = self._attack(allies, enemies)
            interruptible = self.windingup
        elif self.attacking:
            self.attacking = self.timers_ms[ATTACK] > 0
            interruptible = self.attacking
            need_new_action = not self.attacking
        elif self.casting:
            self.casting = self.timers_ms[CAST] > 0
            if not self.casting:
                action = self._ability(allies, enemies, bench)
                need_new_action = True
        elif self.channeling:
            self.channeling = self.timers_ms[CHANNEL] > 0
            if self.channeling:
                action = self._ability(allies, enemies, bench)
            else:
                need_new_action = True

        # evaluate next action
        if (
            (interruptible or need_new_action)
            and (self.mp >= self.mp_max)
            and self._getset_ability_target()
        ):
            self.mp = min(self.mp - self.mp_max, self.mp_max)
            self.timers_ms[[CAST, MANALOCK]] = CAST_MS, MANALOCK_MS
            self.casting = True
            self.manalocked = True
        elif need_new_action:
            if self._getset_attack_target():
                atk_timer_ms = 1000.0 / self.atk_spd
                self.timers_ms[ATTACK] = atk_timer_ms
                self.timers_ms[WINDUP] = atk_timer_ms * (1 - WINDUP_PERCENT)
                self.windingup = True
                self.attacking = True
            else:
                # TODO
                self.moving = True

        # decrement timers and return
        self.timers_ms = np.clip(
            np.subtract(self.timers_ms, TICK_MS, out=self.timers_ms),
            a_min=0,
            a_max=None,
            out=self.timers_ms,
        )
        return action
