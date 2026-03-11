from settings import *
from pygame import Surface
from entities.Creatures import Creature
from utils.Helper import get_frect


class Monster ( pygame.sprite.Sprite, Creature ):
	def __init__(self, name: Monsters, image: Surface, **anchor: tuple[float, float]) -> None:
		super().__init__()

		self.image = image
		self.rect = get_frect(self.image, **anchor)
		self.get_data(name)
