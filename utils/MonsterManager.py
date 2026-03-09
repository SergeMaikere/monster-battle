from functools import partial
from typing import cast
from settings import *
from pygame.sprite import Group
from random import choice, sample
from entities.Monster import Monster
from entities.Opponent import Opponent
from utils.Helper import folder_importer, pipe


class MonsterManager:
    _instance = None

    def __init__ ( self, all_sprites: Group ):
        if not hasattr(self, 'initialized'):

            self.all_sprites = all_sprites

            self.monsters_back = folder_importer('assets', 'images', 'back')
            self.monsters_front = folder_importer('assets', 'images', 'front')
            self.monsters_minis = folder_importer('assets', 'images', 'simple')

            self.player_monsters = [ Monster( name, self.monsters_back[name], bottomleft=(100, WINDOW_HEIGHT) ) for name in self.__get_sample_monsters_names(2) ]
            self.player_monster: Monster = self.player_monsters[0]
            self.opponent_monster = self.make_opponent_monster()

            self.initialized = True


    def __new__ ( cls, *args, **kwargs ):
        if not cls._instance:
            cls._instance = super(MonsterManager, cls).__new__(cls)
        return cls._instance


    def __get_single_monster_name ( self ) -> Monsters:
        name = choice( [name for name in MONSTER_DATA.keys()] )
        print(name)
        if name in Monsters.__args__:
            return cast(Monsters, name)  
        else: 
            raise ValueError('Invalid Monster Name')

    def __get_sample_monsters_names ( self, n: int ) -> list[Monsters]: 
        names = sample(tuple(MONSTER_DATA.keys()), n)
        if all(name in Monsters.__args__ for name in names):
            return cast(list[Monsters], names)
        else:
            raise ValueError('Invalid Monster Name')

    def make_opponent_monster ( self ):
        name = self.__get_single_monster_name()
        return Opponent(name, self.monsters_front[name], self.all_sprites, midbottom=(WINDOW_WIDTH - 250, 300))

    def is_monster_healty ( self, monster: Monster | Opponent ): return monster.health > 0


    def init_player_monster ( self ): self.all_sprites.add(self.player_monster)

    def get_monster_surface ( self, name: Monsters ): return self.monsters_minis[name]

    def __kill_previous_monster ( self, trainer: Literal['player', 'opponent'] ):
        monster = self.player_monster if trainer == 'player' else self.opponent_monster
        monster.kill()

    def __remove_previous_monster_from_all_sprites ( self, trainer: Literal['player', 'opponent'] ):
        sprite = next((sprite for sprite in self.all_sprites if type(sprite) == (Monster if trainer == 'player' else Opponent)), None)
        if sprite: self.all_sprites.remove(sprite)

    def remove_previous_monster ( self, trainer: Literal['player', 'opponent'] ):
        self.__kill_previous_monster(trainer)
        self.__remove_previous_monster_from_all_sprites(trainer)

    def set_player_monster ( self, monster: Monster ):
        self.remove_previous_monster('player')
        self.player_monster = monster
        self.init_player_monster()

    def set_opponent_monster ( self ):
        self.remove_previous_monster('opponent')
        self.opponent_monster = self.make_opponent_monster()
        self.all_sprites.add(self.opponent_monster)

    def has_monsters_left ( self ) -> bool:
        return len([ monster for monster in self.player_monsters if monster.health > 0 ]) > 0

    def get_available_monsters ( self ) -> list[Monsters]: 
        return [ cast(Monsters, monster.name) for monster in self.player_monsters if monster.name != self.player_monster.name and monster.health > 0 ]

    def get_next_available_monster ( self ) -> Monsters:
        return next(cast(Monsters, monster.name) for monster in self.player_monsters if monster.name != self.player_monster.name and monster.health > 0)

    def switch_monster ( self, name: Monsters ):
        monster = next(monster for monster in self.player_monsters if monster.name == name)
        self.set_player_monster(monster)
    
    def __get_ability_datas_by_name ( self, attack: Attacks ): return ABILITIES_DATA[attack]
    
    def __calculate_health_malus ( self, target: Monster | Opponent, ability_data: Ability ) -> float: 
        return ability_data['damage'] * ELEMENT_DATA[ability_data['element']][MONSTER_DATA[target.name]['element']]

    def __substract_damage ( self, target: Monster | Opponent, malus: int ): 
        target.health -= malus
        return malus

    def apply_attack ( self, target: Monster | Opponent, attack: Attacks ):
        malus = pipe( 
            self.__get_ability_datas_by_name, 
            partial(self.__calculate_health_malus, target) ,
            partial(self.__substract_damage, target)
        )(attack)
        print(f'VICTIM: {target.name} -> ATTACK: {attack} DAMAGE: -{malus} CURRENT HEALTH: {target.health} MAX-HEALTH: {target.max_health}')
    
    def heal_monster ( self ): self.player_monster.health += 50

