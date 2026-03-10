from pygame import FRect
from settings import *
from utils.Helper import get_canvas
from utils.MonsterManager import MonsterManager

class Infos:
	def __init__(self, subject: Literal['player', 'opponent'], rect: FRect, monster_manager: MonsterManager) -> None:
		
		self.subject = subject
		self.monster_manager = monster_manager

		self.canvas = get_canvas()
		self.font = pygame.font.Font(None, 30)

		self.info_rect = rect


	def __get_monster ( self ): return self.monster_manager.player_monster if self.subject == 'player' else self.monster_manager.opponent_monster

	def __draw_menu_rect ( self, rect: FRect ):		
		pygame.draw.rect(self.canvas, COLORS['white'], rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], rect, 4, 4)

	def __draw_monster_name ( self ): 
		self.name_surf = self.font.render(self.__get_monster().name, True, COLORS['black'])
		self.name_rect = self.name_surf.get_frect(topleft=self.info_rect.topleft + pygame.Vector2(self.info_rect.width * 0.05, 12))
		self.canvas.blit(self.name_surf, self.name_rect)

	def __draw_health_bar ( self ):
		health_rect = pygame.FRect(self.name_rect.left, self.name_rect.bottom + 10, self.info_rect.width * 0.9, 20 )
		ratio = health_rect.width / self.__get_monster().max_health
		progress_bar = pygame.FRect(health_rect.left, health_rect.top, self.__get_monster().health * ratio, health_rect.height)
		
		pygame.draw.rect(self.canvas, COLORS['gray'], health_rect)
		pygame.draw.rect(self.canvas, COLORS['red'], progress_bar)

	def draw ( self ):
		self.__draw_menu_rect(self.info_rect)
		self.__draw_monster_name()
		self.__draw_health_bar()