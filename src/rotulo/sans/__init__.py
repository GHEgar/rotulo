from rotulo.context import Context
from rotulo.params import Sans
from rotulo.sans.figures import add_figures
from rotulo.sans.kit import Kit
from rotulo.sans.lowercase import add_lowercase
from rotulo.sans.uppercase import add_uppercase

__all__ = ["add_sans"]


def add_sans(ctx: Context, sans: Sans) -> None:
    kit = Kit(ctx, sans)
    add_lowercase(kit)
    add_uppercase(kit)
    add_figures(kit)
