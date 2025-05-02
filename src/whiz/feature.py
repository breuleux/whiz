from functools import reduce
from operator import add

from ovld.utils import clsstring
from serieux.schema import AnnotatedSchema

from .proxy import AugmentedProxy


class Augment(type):
    _cls: type = None
    _aug: type = None

    def __class_getitem__(cls, args):
        if len(args) <= 1:  # pragma: no cover
            raise TypeError("Augment[...] takes at least two arguments")
        base_type, *augmentations = args
        aug = reduce(add, augmentations)
        return type(
            f"Augment[{clsstring(base_type)}, {clsstring(aug)}]",
            (Augment,),
            {"__module__": None, "_cls": base_type, "_aug": aug},
        )

    @classmethod
    def serieux_deserialize(cls, obj, ctx, call_next):
        if isinstance(obj, dict) and "$value" in obj:
            obj = dict(obj)
            value = obj.pop("$value")
            aug = call_next(cls._aug, obj, ctx)
            return AugmentedProxy(call_next(cls._cls, value, ctx), aug)
        else:
            return call_next(cls._cls, obj, ctx)

    @classmethod
    def serieux_serialize(cls, obj, ctx, call_next):
        if type(obj) is AugmentedProxy:
            return {
                "$value": call_next(cls._cls, obj.__wrapped__, ctx),
                **call_next(cls._aug, obj._, ctx),
            }
        else:
            return call_next(cls._cls, obj, ctx)

    @classmethod
    def serieux_schema(cls, ctx, call_next):
        return AnnotatedSchema(
            parent=call_next(cls._aug, ctx),
            properties={"$value": call_next(cls._cls, ctx)},
            required=["$value"],
        )
