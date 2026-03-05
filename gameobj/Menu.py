from typing import Any, Callable
from settings import *
from functools import partial
from pygame import FRect
from utils.Helper import get_canvas, pipe


class Menu:
	def __init__( 
		self, 
		state: State, 
		rect: FRect, 
		options: list[str], 
		menu_index: RowCol, 
		rows_cols: Table, 
		get_monster_list: Callable | None = None,
		get_monster_surface: Callable | None = None) -> None:

		self.state = state
		self.rect = rect
		self.rows, self.cols = rows_cols['rows'], rows_cols['cols']
		self.cell_width, self.cell_height = self.__get_width_height()

		self.options = options
		self.menu_index = menu_index
		self.get_monster_surface = get_monster_surface
		self.get_monster_list = get_monster_list

		self.canvas = get_canvas()
		self.font = pygame.font.Font(None, 30)
		self.vertical_offset = 0

	def __get_width_height ( self ): return ( self.rect.width / self.cols, self.rect.height / self.rows )

	def __draw_menu_rect ( self ):		
		pygame.draw.rect(self.canvas, COLORS['white'], self.rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], self.rect, 4, 4)

	def __set_vertical_offset ( self, row_col: tuple[int, int] ):
		row, col = row_col
		self.vertical_offset = 0 if self.menu_index['row'] < self.rows else -(self.menu_index['row'] - self.rows + 1) * (self.rect.height / self.rows)
		return row_col

	def __get_text_color ( self, row_col: tuple[int, int] ):
		row, col = row_col
		return { 'color': COLORS['gray'] if row == self.menu_index['row'] and col == self.menu_index['col'] else COLORS['black'] }

	def __get_text_surface ( self, index: int, menu_data: dict[str, Any] ):
		return { 'text_surface': self.font.render(self.options[index], True, menu_data['color']) }

	def __get_mini_surface ( self, index: int ): 
		if not self.get_monster_surface: raise Exception('List of player monster missing')
		return { 'mini_surface': self.get_monster_surface(self.options[index]) }
		
	def __get_cell_pos_x ( self, item: Literal['mini', 'text'] ):
		if item == 'mini': return self.cell_width * 1/3
		return self.cell_width * 2/3
	
	
	def __get_item_position ( self, row_col: tuple[int, int], item: Literal['mini', 'text'], menu_data: dict[str, Any] ):
		row, col = row_col
		x = self.rect.left + self.__get_cell_pos_x(item)  + col * self.cell_width
		y = self.rect.top + self.cell_height / 2 + row * self.cell_height + self.vertical_offset
		return { **menu_data, 'pos': (x, y) }

	def __get_text_rect ( self, menu_data: dict[str, Any] ):
		return { **menu_data, 'text_rect': menu_data['text_surface'].get_frect(center=menu_data['pos']) }

	def __get_mini_rect ( self, menu_data: dict[str, Any] ):
		return { **menu_data, 'mini_rect': menu_data['mini_surface'].get_frect(center=menu_data['pos']) }


	def __draw_menu_item ( self, item: Literal['mini', 'text'], menu_data: dict[str, Any] ):
		if self.rect.collidepoint(menu_data['pos']):
			if item == 'text': self.canvas.blit(menu_data['text_surface'], menu_data['text_rect'])
			if item == 'mini': self.canvas.blit(menu_data['mini_surface'], menu_data['mini_rect'])

	def __set_menu_text ( self, row_col: tuple[int, int], index: int ):
		pipe(
			self.__set_vertical_offset,
			self.__get_text_color,
			partial(self.__get_text_surface, index),
			partial(self.__get_item_position, (row_col), 'text'),
			self.__get_text_rect,
			partial(self.__draw_menu_item, 'text')
		)( (row_col) )

	def __set_menu_pics ( self, row_col: tuple[int, int], index: int ):
		pipe(
			self.__get_mini_surface,
			partial(self.__get_item_position, row_col, 'mini'),
			self.__get_mini_rect,
			partial(self.__draw_menu_item, 'mini')
		)(index)


	def __draw_menu_options ( self ):
		i = 0
		for row in range(self.rows if self.state != 'switch' else len(self.options)):
			for col in range(self.cols):

				if self.state == 'switch' and self.get_monster_list:
					self.options = self.get_monster_list() 
					self.__set_menu_pics((row, col), i)
				self.__set_menu_text((row, col), i)
				i += 1

	def draw ( self ):
		self.__draw_menu_rect()
		self.__draw_menu_options()


