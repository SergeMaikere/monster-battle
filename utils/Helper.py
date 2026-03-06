from settings import *
from functools import reduce
from pygame.surface import Surface
from utils.Errors import NoDisplaySurface 

pipe = lambda *func: lambda arg: reduce( lambda g, f: f(g), func, arg )

def get_canvas () -> Surface:
    canvas = pygame.display.get_surface()
    if not canvas: raise NoDisplaySurface()
    return canvas

def folder_importer(*path: str) -> dict[str, Surface]:
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict