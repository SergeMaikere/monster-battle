from typing import TypedDict

from pygame.typing import ColorLike
from settings import *
from functools import partial
from pygame import K_DOWN, FRect, Surface
from entities.Monster import Monster
from utils.Errors import NoDisplaySurface
from utils.Helper import pipe

class RowCol ( TypedDict ):
	row: int
	col: int

class Menu:
	def __init__( self, rect: FRect, options: list[str], menu_index: RowCol, rows_cols: tuple[int, int] ) -> None:

		self.canvas = pygame.display.get_surface()
		self.font = pygame.font.Font(None, 30)

		self.rect = rect
		self.rows, self.cols = rows_cols
		self.options = options
		self.menu_index = menu_index

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

	def __get_text_color ( self, row_col: tuple[int, int] ):
		row, col = row_col
		return COLORS['gray'] if row == self.menu_index['row'] and col == self.menu_index['col'] else COLORS['black']

	def __get_text_surface ( self, color: ColorLike, index: int ):
		return self.font.render(self.options[index], True, color)

	def __get_text_rect ( self, pos: tuple[float, float], text_surface: Surface ): 
		text_rect = text_surface.get_frect(center=pos)
		return ( text_surface, text_rect )

	def __get_text_surface_and_rect ( self, row_col: tuple[int, int] ):
		pos = self.__get_text_pos(row_col)
		color = self.__get_text_color(row_col)
		return pipe(
			self.__get_index,
			partial(self.__get_text_surface, color),
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
		self.general_dimensions = (2, 2)
		self.general_index: RowCol = { 'row': 0, 'col': 0 }
		self.general_menu = Menu( pygame.FRect(self.left, self.top, 400, 200), self.general_options, self.general_index, self.general_dimensions )

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ) % self.general_dimensions[0]
		self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) ) % self.general_dimensions[1]
		print(self.general_index)

	def update ( self ):
		self.__input()

	def draw ( self ):
		self.general_menu.draw()
