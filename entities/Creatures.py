from settings import *
from random import sample

class Creature ():
	def get_data ( self, name: Monsters ):
		self.name = name
		self.element = MONSTER_DATA[name]['element']
		self.health = MONSTER_DATA[name]['health']
		self.abilities = sample(tuple(ABILITIES_DATA.keys()), 4)