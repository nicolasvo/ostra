from apistar import types
from apistar.validators import String


class Data(types.Type):
    word = String(min_length=5,
                  description="Word to translate (from russian to english)",
                  allow_null=False)
