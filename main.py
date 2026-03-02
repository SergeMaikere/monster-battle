from typing import Union, cast, get_args
from entities.Opponent import Opponent
from entities.Monster import Monster
from gameobj.Menus import Menus
from settings import *
from utils.Helper import folder_importer
from random import sample, choice

class Game ():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('MONSTER BATTLE IV --> Surviving Sacha #Mew-2')
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.bg_images = folder_importer('assets', 'images', 'other')
        self.monsters_back = folder_importer('assets', 'images', 'back')
        self.monsters_front = folder_importer('assets', 'images', 'front')
        self.monsters_minis = folder_importer('assets', 'images', 'simple')

        self.player_monster_list = sample(tuple(MONSTER_DATA.keys()), 6)
        self.player_monsters = [ Monster( name, self.monsters_back[name], bottomleft=(100, WINDOW_HEIGHT) ) for name in self.player_monster_list ]
        
        self._player_monster = self.player_monsters[0]
        self._opponent_name = choice(tuple(MONSTER_DATA.keys()))

        self.menu = Menus(self.player_monster, self.player_monsters, self.__get_monster_surface, self.__get_input)

        self.running = True

    @property
    def player_monster ( self ):
        return self._player_monster

    @player_monster.setter
    def player_monster ( self, monster: Monster ):
        self.remove_previous_monster('player')
        self.all_sprites.add(monster)
        self._player_monster = monster

    @property
    def opponent_name ( self ):
        return self._opponent_name

    @opponent_name.setter
    def opponent_name ( self, name: str ):
        # self.remove_previous_monster('opponent')
        self._opponent_name = name
        self.opponent_monster = Opponent(self._opponent_name, self.monsters_front[self._opponent_name], self.all_sprites, midbottom=(WINDOW_WIDTH - 250, 300))

    def __get_monster_surface ( self, name: Monsters ): return self.monsters_minis[name]

    def __apply_attack ( self, attack: Attacks ):
        assert type(attack) == Attacks, 'Invalid attack'
        print(attack)

    def __switch_monster ( self, name: Monsters ):
        self.player_monster = next(monster for monster in self.player_monsters if monster.name == name)
        self.menu.monster = self.player_monster
    
    def __heal_monster ( self, name: Monsters ):
        print(name)
        return name

    def __end_game ( self ): self.running = False

    def __get_input ( self, state: State, data: Attacks | Monsters ):
        if state == 'attack' and data in Attacks.__args__: return self.__apply_attack(cast(Attacks, data))
        if state == 'switch' and data in Monsters.__args__: return self.__switch_monster(cast(Monsters, data))
        if state == 'general' and data == 'heal': return self.__heal_monster(data)
        if state == 'general' and data == 'escape': return self.__end_game()
    

    def __set_background ( self ):
        self.canvas.blit(self.bg_images['bg'], (0, 0))

    def __draw_monster_floor ( self ):
        for monster in self.all_sprites:
            floor_rect = self.bg_images['floor'].get_frect(center=monster.rect.midbottom + pygame.Vector2(0, -10))
            self.canvas.blit(self.bg_images['floor'], floor_rect)

    def remove_previous_monster ( self, trainer: Literal['player', 'opponent'] ):
        old_monster_name = self.player_monster.name if trainer == 'player' else self.opponent_monster.name
        for sprite in self.all_sprites:
            if sprite.name == old_monster_name:
                self.all_sprites.remove(sprite)

    def __init_combattants ( self ):
        self.player_monster = self.player_monsters[0]
        self.opponent_name = self.opponent_name

    def run ( self ):

        self.__init_combattants()

        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.running = not event.type == pygame.QUIT

            self.__set_background()

            self.__draw_monster_floor()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.canvas)

            self.menu.update()
            self.menu.draw()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    new_game = Game()
    new_game.run()