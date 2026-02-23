from settings import *
from functools import partial
from pygame import FRect, Surface
from entities.Monster import Monster
from utils.Errors import NoDisplaySurface
from utils.Helper import pipe


class Menu:
	def __init__( self, rect: FRect, cols: int, rows: int, options: list[str] ) -> None:

		self.canvas = pygame.display.get_surface()
		self.font = pygame.font.Font(None, 30)

		self.rect = rect
		self.cols = cols
		self.rows = rows
		self.options = options

	def __draw_menu_rect ( self ):
		if not self.canvas: raise NoDisplaySurface()
		
		pygame.draw.rect(self.canvas, COLORS['white'], self.rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], self.rect, 4, 4)

	def __get_index ( self, row_col: tuple[int, int] ): 
		row, col = row_col
		return col + row * self.cols

	def __get_text_pos ( self, row_col: tuple[int, int] ):
		row, col = row_col
		x = self.rect.left + self.rect.width / (self.cols * 2) + col * (self.rect.width / self.cols)
		y = self.rect.top + self.rect.height / (self.rows * 2) + row * (self.rect.height / self.rows)
		return (x, y)

	def __get_text_surface ( self, index: int ):
		return self.font.render(self.options[index], True, COLORS['black'])

	def __get_text_rect ( self, pos: tuple[float, float], text_surface: Surface ): 
		text_rect = text_surface.get_frect(center=pos)
		return ( text_surface, text_rect )

	def __get_text_surface_and_rect ( self, row_col: tuple[int, int] ):
		pos = self.__get_text_pos(row_col)
		return pipe(
			self.__get_index,
			self.__get_text_surface,
			partial(self.__get_text_rect, pos)
		)(row_col)

	def __draw_menu_option ( self, text_surface: Surface, text_rect: FRect ):
		if not self.canvas: raise NoDisplaySurface()
		self.canvas.blit(text_surface, text_rect)

	def __draw_menu_options ( self ):

		for row in range(self.rows):
			for col in range(self.cols):
				text_surface, text_rect = self.__get_text_surface_and_rect((row, col))
				self.__draw_menu_option(text_surface, text_rect)

	def draw ( self ):
		self.__draw_menu_rect()
		self.__draw_menu_options()



class Menus:
	def __init__( self, monster: Monster ) -> None:

		self.canvas = pygame.display.get_surface()
		
		self.left = WINDOW_WIDTH/2 - 100
		self.top = WINDOW_HEIGHT/2 + 50

		self.monster = monster

		self.general_options = [ 'attack', 'heal', 'switch', 'escape' ]
		self.general_menu = Menu( pygame.FRect(self.left, self.top, 400, 200), 2, 2, self.general_options )


	def draw ( self ):
		self.general_menu.draw()
