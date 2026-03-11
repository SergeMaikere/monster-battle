from settings import *
from pygame import Surface
from pygame.sprite import Group
from entities import Opponent as o, Monster as m

class AttackAnimation ( pygame.sprite.Sprite ):
	def __init__(self, monster: m.Monster | o.Opponent, frames: list[Surface], *groups: Group) -> None:
		super().__init__(*groups)

		self.frames = frames
		self.index = 0
		self.image = self.frames[self.index]
		self.rect = self.image.get_frect(center=monster.rect.center)

	def update ( self, dt: float ):
		self.index += 5 * dt
		if self.index < len(self.frames):
			self.image = self.frames[int(self.index)]
		else:
			self.kill()