from pygame.typing import ColorLike
from settings import *
from functools import partial
from pygame import FRect, Surface
from utils.Errors import NoDisplaySurface
from utils.Helper import pipe


class Menu:
	def __init__( 
		self, 
		state: State, 
		rect: FRect, 
		options: list[str], 
		menu_index: RowCol, 
		rows_cols: tuple[int, int], 
		monsters_minis: dict[str, Surface] | None = None ) -> None:

		self.state = state
		self.rect = rect
		self.rows, self.cols = rows_cols
		self.options = options
		self.menu_index = menu_index

		self.canvas = pygame.display.get_surface()
		self.font = pygame.font.Font(None, 30)
		self.vertical_offset = 0

	def __draw_menu_rect ( self ):
		if not self.canvas: raise NoDisplaySurface()
		
		pygame.draw.rect(self.canvas, COLORS['white'], self.rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], self.rect, 4, 4)

	def __set_vertical_offset ( self, row_col: tuple[int, int] ):
		row, col = row_col
		self.vertical_offset = 0 if self.menu_index['row'] < self.rows else -(self.menu_index['row'] - self.rows + 1) * (self.rect.height / self.rows)
		return row_col

	def __get_index ( self, row_col: tuple[int, int] ): 
		row, col = row_col
		return col + row * self.cols

	def __get_text_pos ( self, row_col: tuple[int, int] ):
		row, col = row_col
		x = self.rect.left + self.rect.width / (self.cols * 2) + col * (self.rect.width / self.cols)
		y = self.rect.top + self.rect.height / (self.rows * 2) + row * (self.rect.height / self.rows) + self.vertical_offset
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
			self.__set_vertical_offset,
			self.__get_index,
			partial(self.__get_text_surface, color),
			partial(self.__get_text_rect, pos)
		)(row_col)

	def __draw_menu_option ( self, text_surface: Surface, text_rect: FRect ):
		if not self.canvas: raise NoDisplaySurface()

		if self.rect.collidepoint(text_rect.center):
			self.canvas.blit(text_surface, text_rect)

	def __draw_menu_options ( self ):
		for row in range(self.rows if self.state != 'switch' else len(self.options)):
			for col in range(self.cols):

				text_surface, text_rect = self.__get_text_surface_and_rect((row, col))
				self.__draw_menu_option(text_surface, text_rect)

	def draw ( self ):
		self.__draw_menu_rect()
		self.__draw_menu_options()
