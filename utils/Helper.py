from pygame import SRCALPHA, FRect, SurfaceType
from settings import *
from functools import reduce
from pygame.surface import Surface
from utils.Errors import NoDisplaySurface 

pipe = lambda *func: lambda arg: reduce( lambda g, f: f(g), func, arg )

def get_canvas () -> Surface:
    canvas = pygame.display.get_surface()
    if not canvas: raise NoDisplaySurface()
    return canvas

def folder_importer ( *path: str ) -> dict[str, Surface]:
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer ( *path: str ):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict

def cut_animation ( surface: Surface, width: float, col: int ):
    cut_surface = pygame.Surface((width, surface.get_height()), pygame.SRCALPHA)
    cut_rect = pygame.FRect(width * col, 0, width, surface.get_height())
    cut_surface.blit(surface, (0, 0), cut_rect)
    return cut_surface

def tile_importer ( cols: int, *path: str ) -> dict[str, list[Surface]]:
    attack_anim = {}
    for folder_path, _, files in walk(join(*path)):
        for file in files:
            anim_surface = pygame.image.load(join(folder_path, file)).convert_alpha()
            width_cut = anim_surface.get_width() / cols
            attack_anim[file.split('.')[0]] = [ cut_animation(anim_surface, width_cut, col) for col in range(cols) ]
    return attack_anim


def get_frect ( surface: Surface, **anchor: tuple[float, float] ) -> FRect: 
    rect = surface.get_frect(**anchor)
    if rect: return cast(FRect, rect)
    raise ValueError('Surface could not create rectangle')