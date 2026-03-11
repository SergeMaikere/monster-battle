from settings import *
from random import sample

class Creature ():
	def get_data ( self, name: Monsters ):
		self.name = name
		self.element = MONSTER_DATA[name]['element']
		self.max_health = self._health = MONSTER_DATA[name]['health']
		self.abilities = sample(tuple(ABILITIES_DATA.keys()), 4)


	@property
	def health ( self ): return self._health

	@health.setter
	def health ( self, n: int ):
		self._health = min(max(0, n), self.max_health)