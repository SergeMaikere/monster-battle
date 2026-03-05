from functools import partial
from typing import Any, Callable
from pygame import FRect
from pygame.typing import ColorLike
from settings import *
from gameobj.Menu import Menu
from utils.Helper import get_canvas, pipe

class SwitchMenu:
	def __init__(self, 
		state: State, 
		rect: FRect, 
		options: list[str], 
		get_menu_index: Callable,
		rows_cols: Table, 
		get_monster_list: Callable, 
		get_monster_surface: Callable) -> None:

		self.state = state
		self.rect = rect
		self.rows, self.cols = rows_cols['rows'], rows_cols['cols']
		self.cell_width, self.cell_height = self.__get_width_height()

		self.options = options
		self.get_menu_index = get_menu_index
		self.get_monster_surface = get_monster_surface
		self.get_monster_list = get_monster_list

		self.canvas = get_canvas()
		self.font = pygame.font.Font(None, 30)
		self.vertical_offset = 0

	
	def __get_width_height ( self ): return ( self.rect.width / self.cols, self.rect.height / self.rows )

	def __set_vertical_offset ( self, row: int ):
		self.vertical_offset = 0 if self.get_menu_index() < self.rows else -(self.get_menu_index() - self.rows + 1) * (self.rect.height / self.rows)
		return row

	def __get_text_color ( self, row: int ):
		return { 'color': COLORS['gray'] if row == self.get_menu_index() else COLORS['black'] }

	def __get_text_surface ( self, index: int, menu_data: dict[str, Any] ):
		return { 'text_surface': self.font.render(self.options[index], True, menu_data['color']) }

	def __get_cell_pos_x ( self, item: Literal['mini', 'text'] ):
		if item == 'mini': return self.cell_width * 1/3
		return self.cell_width * 2/3

	def __get_item_position ( self, index: int, item: Literal['mini', 'text'], menu_data: dict[str, Any] ):
		x = self.rect.left + self.__get_cell_pos_x(item)
		y = self.rect.top + self.cell_height / 2 + self.cell_height * index + self.vertical_offset
		return { **menu_data, 'pos': (x, y) }

	def __get_rect ( self, item: Literal['mini', 'text'], menu_data: dict[str, Any] ):
		if item == 'text': return { **menu_data, 'text_rect': menu_data['text_surface'].get_frect(center=menu_data['pos']) }
		if item == 'mini': return { **menu_data, 'mini_rect': menu_data['mini_surface'].get_frect(center=menu_data['pos']) }

	def __draw_menu_item ( self, item: Literal['mini', 'text'], menu_data: dict[str, Any] ):
		if self.rect.collidepoint(menu_data['pos']):
			if item == 'text': self.canvas.blit(menu_data['text_surface'], menu_data['text_rect'])
			if item == 'mini': self.canvas.blit(menu_data['mini_surface'], menu_data['mini_rect'])

	def __get_mini_surface ( self, index: int ): 
		return { 'mini_surface': self.get_monster_surface(self.options[index]) }


	def __draw_menu_rect ( self ):		
		pygame.draw.rect(self.canvas, COLORS['white'], self.rect, 0, 4)
		pygame.draw.rect(self.canvas, COLORS['gray'], self.rect, 4, 4)

	def __draw_menu_options ( self ):
		for row in range(len(self.options)):
			pipe(
				self.__set_vertical_offset,
				self.__get_text_color,
				partial(self.__get_text_surface, row),
				partial(self.__get_item_position, row, 'text'),
				partial(self.__get_rect, 'text'),
				partial(self.__draw_menu_item, 'text')
			)(row)

			pipe(
				self.__get_mini_surface,
				partial(self.__get_item_position, row, 'mini'),
				partial(self.__get_rect, 'mini'),
				partial(self.__draw_menu_item, 'mini')
			)(row)

	def draw ( self ):
		self.__draw_menu_rect()
		self.__draw_menu_options()