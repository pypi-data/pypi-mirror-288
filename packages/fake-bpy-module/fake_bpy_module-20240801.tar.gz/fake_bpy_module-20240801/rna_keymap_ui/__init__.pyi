import typing
import collections.abc
import typing_extensions

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def draw_entry(display_keymaps, entry, col, level=0): ...
def draw_filtered(display_keymaps, filter_type, filter_text, layout): ...
def draw_hierarchy(display_keymaps, layout): ...
def draw_keymaps(context, layout): ...
def draw_km(display_keymaps, kc, km, children, layout, level): ...
def draw_kmi(display_keymaps, kc, km, kmi, layout, level): ...
