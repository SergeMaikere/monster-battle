from settings import *
from pygame import Surface
from entities.Creatures import Creature
from pygame.sprite import Group


class Opponent ( pygame.sprite.Sprite, Creature ):
	def __init__(self, name: Monsters, image: Surface, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(*groups)

		self.image = image
		self.rect = image.get_frect(**anchor)
		self.get_data(name)