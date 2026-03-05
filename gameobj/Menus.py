from typing import Callable, cast
from settings import *
from pygame import Surface
from pygame.key import ScancodeWrapper
from entities.Monster import Monster
from gameobj.Menu import Menu
from gameobj.SwitchMenu import SwitchMenu


class Menus:
	def __init__( self, monster: Monster, player_monsters: list[Monster], get_monster_mini: Callable, get_input: Callable ) -> None:
		
		self.left = WINDOW_WIDTH/2 - 100
		self.top = WINDOW_HEIGHT/2 + 50

		self.get_input = get_input
		self._monster = monster

		self.state = 'general'

		self.general_options = [ 'attack', 'heal', 'switch', 'escape' ]
		self.general_dimensions = self.__set_table_dimensions(2, 2)
		self.general_index: RowCol = self.__init_index()
		self.general_menu = Menu( 
			'general', 
			pygame.FRect(self.left, self.top, 400, 200), 
			self.general_options, 
			self.general_index, 
			self.general_dimensions 
		)

		self.attack_options = self.monster.abilities
		self.attack_dimensions = self.__set_table_dimensions(2, 2)
		self.attack_index: RowCol = self.__init_index()
		self.attack_menu = Menu( 
			'attack', 
			pygame.FRect(self.left, self.top, 400, 200), 
			self.attack_options, 
			self.attack_index, 
			self.attack_dimensions 
		)

		self.player_monsters = player_monsters
		self.switch_options = self.set_available_monsters()
		self.switch_index = 0
		self.switch_dimensions = self.__set_table_dimensions(4, 1)
		self.switch_menu = SwitchMenu( 
			'switch', 
			pygame.FRect(self.left, self.top - 100, 400, 400),
			self.switch_options, 
			self.get_switch_index,
			self.switch_dimensions, 
			self.set_available_monsters,
			get_monster_mini
		)

	
	@property
	def monster ( self ): return self._monster

	@monster.setter
	def monster ( self, monster: Monster ):
		self._monster = monster
		self.switch_options = self.set_available_monsters()

	def __init_index ( self ) -> RowCol: return { 'row': 0, 'col': 0 }

	def __set_table_dimensions ( self, rows: int, cols: int ) -> Table: return { 'rows': rows, 'cols': cols }

	def set_available_monsters ( self ): 
		return [ monster.name for monster in self.player_monsters if monster.name != self.monster.name and monster.health > 0 ]

	def get_switch_index ( self ): return self.switch_index

	def __get_menu_datas ( self ):
		match self.state:
			case 'attack': return (self.attack_index, self.attack_dimensions, self.attack_options)
			case 'switch': return (self.switch_index, self.switch_dimensions, self.switch_options)
			case _: return (self.general_index, self.general_dimensions, self.general_options)

	def __update_switch_index ( self, keys: ScancodeWrapper, options: list[str] ):
		self.switch_index = ( self.switch_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ) % len(options)
		print('menus', self.switch_index)

	def __update_menu_index ( self, keys: ScancodeWrapper, index: RowCol, table: Table ):
		index['row'] = (index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ) % table['rows']
		index['col'] = (index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) ) % table['cols']

	def __update_index ( self, keys: ScancodeWrapper, index: RowCol | int , options: list[str], table: Table ):
		if self.state == 'switch': return self.__update_switch_index(keys, options)
		return self.__update_menu_index(keys, cast(RowCol, index), table)
	
	def __update_menu_state ( self, index: RowCol, table: Table, options: list[str] ):
		data = options[ index['col'] + index['row'] * table['cols'] ]
		if data in ['attack', 'switch']: 
			self.state = data
		else:
			self.get_input(self.state, options[ index['col'] + index['row'] * table['cols'] ])
			self.state = 'general'


	def __update_state ( self, keys: ScancodeWrapper, index: RowCol | int, table: Table, options: list[str] ):
		if keys[pygame.K_SPACE]: 
			if self.state == 'switch': 
				self.get_input(self.state, options[cast(int, index)])
				self.state = 'general'
			else: 
				self.__update_menu_state(cast(RowCol, index), table, options)
		

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		index, table, options = self.__get_menu_datas()
		self.__update_index(keys, index, options, table)
		self.__update_state(keys, index, table, options)

	def update ( self ):
		self.__input()

	def draw ( self ):
		match self.state:
			case 'general': self.general_menu.draw()
			case 'attack': self.attack_menu.draw()
			case 'switch': self.switch_menu.draw()
