from settings import *
from typing import Any
from pygame import FRect
from gameobj.Menu import Menu
from utils.MonsterManager import MonsterManager

class AttackMenu ( Menu ):
	def __init__(self, rect: FRect, manager: MonsterManager, menu_index: RowCol, rows_cols: Table) -> None:
		super().__init__(rect, manager.player_monster.abilities, menu_index, rows_cols)

		self.manager = manager


	def _get_text_surface ( self, index: int, menu_data: dict[str, Any] ):
		return { 'text_surface': self.font.render(self.manager.player_monster.abilities[index], True, menu_data['color']) }