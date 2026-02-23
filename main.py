from entities.Opponent import Opponent
from entities.Monster import Monster
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

        self.player_monster_list = sample(tuple(MONSTER_DATA.keys()), 4)
        self.player_monsters = [ Monster( name, self.monsters_back[name], bottomleft=(100, WINDOW_HEIGHT) ) for name in self.player_monster_list ]
        
        self._player_monster = None
        self._opponent_name = None

        self.running = True

    @property
    def player_monster ( self ):
        return self._player_monster

    @player_monster.setter
    def player_monster ( self, monster: Monster ):
        # self.remove_previous_monster('player')
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

    def __set_combattants ( self ):
        self.player_monster = self.player_monsters[0]
        self.opponent_name = choice(tuple(MONSTER_DATA.keys()))

    def run ( self ):

        self.__set_combattants()

        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.running = not event.type == pygame.QUIT

            self.__set_background()

            self.__draw_monster_floor()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.canvas)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    new_game = Game()
    new_game.run()