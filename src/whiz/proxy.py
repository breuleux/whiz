from typing import Any

from ovld import Medley, ovld, recurse
from serieux import Context, Serieux
from wrapt import ObjectProxy


class AugmentedProxy(ObjectProxy):
    def __init__(self, wrapped, aug):
        super().__init__(wrapped)
        self._self_ann = aug

    @property
    def _(self):
        return self._self_ann

    def __repr__(self):
        return f"<{self.__wrapped__!r}>"


@Serieux.extend
class HandleProxy(Medley):
    @ovld(priority=-2)
    def serialize(self, t: Any, obj: AugmentedProxy, ctx: Context):
        return recurse(t, obj.__wrapped__, ctx)
