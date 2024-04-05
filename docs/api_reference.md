## `Config`
```py
Charset = Literal["ascii", "alpha", "alnum", "digits"]
BaseKind = Literal["any", "array", "object"]

@dataclass(frozen=True)
class Config:
    # passing an empty tuple will raise an OddsproutValueError
    types: tuple[str, ...] = (
        "int",
        "float",
        "string",
        "boolean",
        "null",
        "array",
        "object",
    )
    base_size: tuple[int, int] = (0, 100)
    string_size: tuple[int, int] = (0, 50)
    collection_size: tuple[int, int] = (0, 100)
    charset: Charset = "ascii"
    base: BaseKind = "any"

    @classmethod
    def from_file(cls, path: PathLike[str] | str) -> Config:
        ...
```
## `JSONGenerator`
```py
type JSONObject = dict[str, JSONValue]
type JSONArray = list[JSONValue]
type JSONValue = JSONObject | JSONArray | str | int | float | bool | None

class JSONGenerator:
    def __init__(self, config: Config | None = None) -> None:
        ...

    @property
    def config(self) -> Config:
        ...

    def generate_value(self) -> JSONValue:
        ...
```