from settings import *
from pygame.sprite import Group
from pygame import Surface
from entities.Creatures import Creature
from utils.Helper import get_frect


class Opponent ( pygame.sprite.Sprite, Creature ):
	def __init__(self, name: Monsters, image: Surface, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(*groups)

		self.image = image
		self.rect = get_frect(self.image, **anchor)
		self.get_data(name)