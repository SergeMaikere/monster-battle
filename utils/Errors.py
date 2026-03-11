
class NoDisplaySurface ( Exception ):
	def __init__(self) -> None:
		self.message = 'Calling pygame.display.get_surface returns None'
		super().__init__(self.message)

