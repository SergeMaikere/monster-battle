from settings import *
from functools import partial
from entities.Monster import Monster
from entities.Opponent import Opponent
from gameobj import AttackAnimation as a
from gameobj.Menus import Menus
from utils.Helper import audio_importer, folder_importer, tile_importer, pipe
from utils.MonsterManager import MonsterManager
from utils.Timer import Timer
from utils.Typeguards import isAttacks, isMonsters, isSound

class Game ():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('MONSTER BATTLE IV --> Surviving Sacha #Mew-2')
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.bg_images = folder_importer('assets', 'images', 'other')
        self.attack_animations = tile_importer(4, 'assets', 'images', 'attacks')
        self.sounds = audio_importer('assets', 'audio')

        self.store = MonsterManager(self.all_sprites)

        self.menu = Menus(self.store, self.__get_input)

        self.timers = { 'player_end': Timer(1000, self.__opponent_turn), 'opponent_end': Timer(1000, self.__player_turn) }
        self.active = True

        self.running = True


    def __update_timers ( self ): 
        for timer in self.timers.values():
            timer.update() 

    def __player_turn ( self ):
        if not self.store.has_monsters_left(): return self.__end_game()

        if not self.store.is_monster_healty(self.store.player_monster):
            self.store.switch_monster(self.store.get_next_available_monster())
        
        self.active = True

    def __opponent_turn ( self ):
        if self.store.is_monster_healty(self.store.opponent_monster):
            self.__attack_beast('player', isAttacks(self.store.get_opponent_attack()))
        else:
            self.store.set_opponent_monster()
        self.timers['opponent_end'].start()

    def __end_game ( self ): self.running = False

    def __apply_attack ( self, monster: Monster | Opponent, attack: Attacks ):
        self.store.apply_attack(monster, attack)
        return attack

    def __get_anim_by_attack ( self, attack: Attacks ): return ABILITIES_DATA[attack]['animation']

    def __create_animation ( self, target: Literal['player', 'opponent'], animation: Animations):
        monster = self.store.player_monster if target == 'player' else self.store.opponent_monster
        a.AttackAnimation(monster, self.attack_animations[animation], self.all_sprites)
        return animation
    
    def __attack_beast ( self, target: Literal['player', 'opponent'], data: Attacks ):
        monster = self.store.player_monster if target == 'player' else self.store.opponent_monster
        pipe(
            partial(self.__apply_attack, monster),
            self.__get_anim_by_attack,
            partial(self.__create_animation, target),
            self.__play_sound
        )(data)       
         

    def __heal_player ( self ):
        self.store.heal_monster()
        a.AttackAnimation(self.store.player_monster, self.attack_animations['green'], self.all_sprites)
        self.__play_sound('green')

    def __get_input ( self, state: State, data: Attacks | Monsters | Literal['heal', 'escape'] ):
        if state == 'attack' and data in Attacks.__args__: self.__attack_beast('opponent', isAttacks(data))
        if state == 'switch' and data in Monsters.__args__: self.store.switch_monster(isMonsters(data))
        if state == 'general' and data == 'heal': self.__heal_player()
        if state == 'general' and data == 'escape': self.__end_game()

        self.active = False
        self.timers['player_end'].start()
        

    def __set_background ( self ):
        self.canvas.blit(self.bg_images['bg'], (0, 0))

    def is_monster_or_opp ( self, o: Any): return isinstance(o, Monster) or isinstance(o, Opponent)

    def __draw_monster_floor ( self ):
        for monster in [ sprite for sprite in self.all_sprites if self.is_monster_or_opp(sprite) ]:
            floor_rect = self.bg_images['floor'].get_frect(center=monster.rect.midbottom + pygame.Vector2(0, -10))
            self.canvas.blit(self.bg_images['floor'], floor_rect)


    def __init_combattants ( self ):
        self.store.init_player_monster()

    def __play_sound ( self, title: Sounds ): self.sounds[title].play()

    def run ( self ):
        self.__play_sound(isSound('music'))

        self.__init_combattants()

        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.running = not event.type == pygame.QUIT

            self.__set_background()

            self.__draw_monster_floor()

            if self.active: self.menu.update()
            self.__update_timers()
            self.all_sprites.update(dt)

            self.all_sprites.draw(self.canvas)
            self.menu.draw()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    new_game = Game()
    new_game.run()