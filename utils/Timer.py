from settings import *
from typing import Callable


class Timer:
	def __init__(self, duration: int, func: Callable | None = None, autostart: bool = False, repeat: bool = False) -> None:
		self.duration = duration
		self.func = func
		self.repeat = repeat

		self.active = autostart
		self.start_time = 0


	def start ( self ):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def stop ( self ):
		self.active = False
		self.start_time = 0
		if self.repeat: self.start()

	def update ( self ):
		if pygame.time.get_ticks() - self.start_time >= self.duration:
			if self.func: self.func()
			self.stop()