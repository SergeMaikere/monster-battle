from settings import *
from utils.Helper import folder_importer

class Game ():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('MONSTER BATTLE IV --> Surviving Sacha #Mew-2')
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.bg_images = folder_importer('assets', 'images', 'other')

        self.running = True

    def __set_background ( self ):
        image = self.bg_images['bg']
        rect = image.get_frect(topleft=(0, 0))
        self.canvas.blit(image, rect)

    def run ( self ):

        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.running = not event.type == pygame.QUIT

            self.__set_background()

            self.all_sprites.update(dt)

            self.all_sprites.draw(self.canvas)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    new_game = Game()
    new_game.run()