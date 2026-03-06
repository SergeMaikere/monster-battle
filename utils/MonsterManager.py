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

            self.player_monsters = [ Monster( name, self.monsters_back[name], bottomleft=(100, WINDOW_HEIGHT) ) for name in self.__get_sample_monsters_names(6) ]
            self.player_monster: Monster = self.player_monsters[0]
            self.opponent_name =  self.__get_sample_monsters_names(1).pop()
            self.opponent_monster = Opponent(self.opponent_name, self.monsters_front[self.opponent_name], self.all_sprites, midbottom=(WINDOW_WIDTH - 250, 300))

            self.initialized = True

    def __new__ ( cls, *args, **kwargs ):
        if not cls._instance:
            cls._instance = super(MonsterManager, cls).__new__(cls)
        return cls._instance


    def __get_sample_monsters_names ( self, n: int ) -> list[Monsters]: 
        names = sample(tuple(MONSTER_DATA.keys()), n)
        if all(name in Monsters.__args__ for name in names):
            return names
        else:
            raise ValueError('Invalid Monster Name')

    def __get_ability_by_name ( self, attack: Attacks ): return ABILITIES_DATA[attack]
    
    def __calculate_health_malus ( self, ability_data: Ability ) -> float: 
        return ability_data['damage'] / ELEMENT_DATA[ability_data['element']][MONSTER_DATA[self.opponent_name]['element']]

    def init_player_monster ( self ): self.all_sprites.add(self.player_monster)

    def get_monster_surface ( self, name: Monsters ): return self.monsters_minis[name]

    def remove_previous_monster ( self, trainer: Literal['player', 'opponent'] ):
        sprite = next((sprite for sprite in self.all_sprites if type(sprite) == (Monster if trainer == 'player' else Opponent)), None)
        if sprite: self.all_sprites.remove(sprite)

    def set_player_monster ( self, monster: Monster ):
        self.remove_previous_monster('player')
        self.all_sprites.add(monster)
        self.player_monster = monster

    def get_avilable_monsters ( self ): 
        return [ monster.name for monster in self.player_monsters if monster.name != self.player_monster.name and monster.health > 0 ]


    def switch_monster ( self, name: Monsters ):
        monster = next(monster for monster in self.player_monsters if monster.name == name)
        self.set_player_monster(monster)

    def apply_attack ( self, target: Monster | Opponent, attack: Attacks ):
        malus = pipe( self.__get_ability_by_name, self.__calculate_health_malus )(attack)
        target.health -= malus
        # print(target.name, self.opponent_monster.health)
    
    def heal_monster ( self ): self.player_monster.health += 20

