from pygame import Surface
from settings import *
from pygame.sprite import Group


class Monster ( pygame.sprite.Sprite ):
	def __init__(self, name: str, image: Surface, **anchor: tuple[float, float]) -> None:
		super().__init__()

		self.name = name
		self.image = image
		self.rect = image.get_frect(**anchor)