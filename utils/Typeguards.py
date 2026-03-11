from functools import partial
from settings import *

T = TypeVar('T')

is_dict = lambda x: isinstance(x, dict)

has_all_attributes = lambda my_keys, my_dict: all( hasattr(my_dict, k) for k in my_keys ) 

has_all_values_same_type = lambda t, my_dict: all( type(v) == t for v in my_dict.values() ) 

all_is_good = lambda *funcs: lambda args: all( f(args) for f in funcs)

def isMonsters ( name: str ):
	if name in Monsters.__args__:
		return cast(Monsters, name)
	else:
		raise ValueError('Invalid monster name')

def isAttacks ( name: str ):
	if name in Attacks.__args__:
		return cast(Attacks, name)
	else:
		raise ValueError('Invalid attack name')

def isSound ( title: str ) -> Sounds:
	if title in Sounds.__args__:
		return cast(Sounds, title)
	else:
		raise ValueError('Invalid sound filename')

def isInt ( n: Any ) -> int:
	if type(n) == int: return cast(int, n)
	raise TypeError("This ain't no int")


def isRowCol ( my_dict: Any ):
	if all_is_good(is_dict, partial(has_all_attributes, ['row', 'col']), partial(has_all_values_same_type, int)):
		return cast(RowCol, my_dict)
	else: raise TypeError("This ain't no RowCol")