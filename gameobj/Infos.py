from pygame import FRect
from entities import Opponent as O, Monster as M
from settings import *
from utils.Helper import get_canvas
from utils.MonsterManager import MonsterManager

class Infos:
	def __init__(self, subject: Literal['player', 'opponent'], rect: FRect, monster_manager: MonsterManager) -> None:
		
		self.monster = monster_manager.player_monster if subject == 'player' else monster_manager.opponent_monster
		self.menu_rect = rect

		self.canvas = get_canvas()
		self.font = pygame.font.Font(None, 30)

		self.info_rect = pygame.FRect(self.menu_rect.left -20, self.menu_rect.top -60, 250, 80)
		self.name_surf = self.font.render(self.monster.name, True, COLORS['black'])
		self.name_rect = self.name_surf.get_frect(topleft=self.info_rect.topleft + pygame.Vector2(self.info_rect.width * 0.05, 12))

		self.health_rect = pygame.FRect(self.name_rect.left, self.name_rect.bottom + 10, self.info_rect.width * 0.9, 20 )
		self.ratio = self.health_rect.width / self.monster.max_health

	def __draw_menu_rect ( self, rect: FRect ):		
		pygame.draw.rect(self.canvas, COLORS['white'], rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], rect, 4, 4)

	def __draw_monster_name ( self ): self.canvas.blit(self.name_surf, self.name_rect)

	def __draw_health_bar ( self ):
		progress_bar = pygame.FRect(self.health_rect.left, self.health_rect.top, self.monster.health * self.ratio, self.health_rect.height)
		pygame.draw.rect(self.canvas, COLORS['gray'], self.health_rect)
		pygame.draw.rect(self.canvas, COLORS['red'], progress_bar)

	def draw ( self ):
		self.__draw_menu_rect(self.info_rect)
		self.__draw_monster_name()
		self.__draw_health_bar()