from typing import Callable
from settings import *
from pygame import Surface
from pygame.key import ScancodeWrapper
from entities.Monster import Monster
from gameobj.Menu import Menu


class Menus:
	def __init__( self, monster: Monster, player_monsters: list[Monster], get_monster_mini: Callable, get_input: Callable ) -> None:
		
		self.left = WINDOW_WIDTH/2 - 100
		self.top = WINDOW_HEIGHT/2 + 50

		self.get_input = get_input
		self.monster = monster

		self.state = 'general'

		self.general_options = [ 'attack', 'heal', 'switch', 'escape' ]
		self.general_dimensions = (2, 2)
		self.general_index: RowCol = self.__init_index()
		self.general_menu = Menu( 
			'general', 
			pygame.FRect(self.left, self.top, 400, 200), 
			self.general_options, 
			self.general_index, 
			self.general_dimensions 
		)

		self.attack_options = self.monster.abilities
		self.attack_dimensions = (2, 2)
		self.attack_index: RowCol = self.__init_index()
		self.attack_menu = Menu( 
			'attack', 
			pygame.FRect(self.left, self.top, 400, 200), 
			self.attack_options, 
			self.attack_index, 
			self.attack_dimensions 
		)

		self.player_monsters = player_monsters
		self.switch_options = self.__get_available_monsters()
		self.switch_dimensions = (4, 1)
		self.switch_index: RowCol = self.__init_index()
		self.switch_menu = Menu( 
			'switch', 
			pygame.FRect(self.left, self.top - 100, 400, 400),
			self.switch_options, 
			self.switch_index, 
			self.switch_dimensions, 
			get_monster_mini
		)

	
	def __init_index ( self ) -> RowCol: return { 'row': 0, 'col': 0 }

	def __get_available_monsters ( self ): 
		return [ monster.name for monster in self.player_monsters if monster.name != self.monster.name and monster.health > 0 ]

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
		if keys[pygame.K_SPACE]: 
			data = options[ index['col'] + index['row'] * dimensions[1] ]
			if data in ['attack', 'switch']: 
				self.state = data
			else:
				self.get_input(self.state, options[ index['col'] + index['row'] * dimensions[1] ])
				self.state = 'general'
		

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
