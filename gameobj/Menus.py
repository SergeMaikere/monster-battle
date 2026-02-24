from typing import TypedDict

from pygame.key import ScancodeWrapper
from pygame.typing import ColorLike
from settings import *
from functools import partial
from pygame import K_DOWN, FRect, Surface
from entities.Monster import Monster
from utils.Errors import NoDisplaySurface
from utils.Helper import pipe

State = Literal[ 'general', 'attack', 'switch' ]

class RowCol ( TypedDict ):
	row: int
	col: int

class Menu:
	def __init__( self, state: State, rect: FRect, options: list[str], menu_index: RowCol, rows_cols: tuple[int, int] ) -> None:

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



class Menus:
	def __init__( self, monster: Monster, player_monsters: list[Monster] ) -> None:

		self.canvas = pygame.display.get_surface()
		
		self.left = WINDOW_WIDTH/2 - 100
		self.top = WINDOW_HEIGHT/2 + 50

		self.monster = monster

		self.state = 'general'

		self.general_options = [ 'attack', 'heal', 'switch', 'escape' ]
		self.general_dimensions = (2, 2)
		self.general_index: RowCol = self.__init_index()
		self.general_menu = Menu( 'general', pygame.FRect(self.left, self.top, 400, 200), self.general_options, self.general_index, self.general_dimensions )

		self.attack_options = self.monster.abilities
		self.attack_dimensions = (2, 2)
		self.attack_index: RowCol = self.__init_index()
		self.attack_menu = Menu( 'attack', pygame.FRect(self.left, self.top, 400, 200), self.attack_options, self.attack_index, self.attack_dimensions )

		self.player_monsters = player_monsters
		self.switch_options = self.__get_available_monsters()
		self.switch_dimensions = (4, 1)
		self.switch_index: RowCol = self.__init_index()
		self.switch_menu = Menu( 'switch', pygame.FRect(self.left, self.top - 100, 400, 400), self.switch_options, self.switch_index, self.switch_dimensions )

	
	def __init_index ( self ) -> RowCol: return { 'row': 0, 'col': 0 }

	def __get_available_monsters ( self ): return [ monster.name for monster in self.player_monsters if monster.name != self.monster.name and monster.health > 0 ]

	def __get_menu_datas ( self ):
		match self.state:
			case 'attack': return (self.attack_index, self.attack_dimensions, self.attack_options)
			case 'switch': return (self.switch_index, self.switch_dimensions, self.switch_options)
			case _: return (self.general_index, self.general_dimensions, self.general_options)

	def __update_switch_index ( self, keys: ScancodeWrapper, index: RowCol, options: list[str] ):
		index['row'] = (index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ) % len(options)

	def __update_index ( self, keys: ScancodeWrapper, index: RowCol, options: list[str], dimensions: tuple[int, int] ):
		if self.state == 'switch': return self.__update_switch_index(keys, index, options)
		index['row'] = (index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ) % dimensions[0]
		index['col'] = (index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) ) % dimensions[1]

	def __update_state ( self, keys: ScancodeWrapper, index: RowCol, dimensions: tuple[int, int], options: list[str] ):
		if keys[pygame.K_SPACE]: self.state = options[ index['col'] + index['row'] * dimensions[1] ]
		if keys[pygame.K_ESCAPE]: self.state = 'general'

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		index, dimensions, options = self.__get_menu_datas()
		self.__update_index(keys, index, options, dimensions)
		self.__update_state(keys, index, dimensions, options)

	def update ( self ):
		self.__input()

	def draw ( self ):
		match self.state:
			case 'general': self.general_menu.draw()
			case 'attack': self.attack_menu.draw()
			case 'switch': self.switch_menu.draw()
