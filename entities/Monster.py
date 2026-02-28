from pygame import Surface
from entities.Creatures import Creature
from settings import *
from pygame.sprite import Group


class Monster ( pygame.sprite.Sprite, Creature ):
	def __init__(self, name: str, image: Surface, **anchor: tuple[float, float]) -> None:
		super().__init__()

		self.image = image
		self.rect = image.get_frect(**anchor)
		self.get_data(name)