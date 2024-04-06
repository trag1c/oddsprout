Oddsprout can be configured via a TOML file (for the CLI) and via a `Config`
object (for the Python library).

## Default config

If left unspecified, the default oddsprout config is equivalent to:

=== "CLI"

    ```toml
    [bounds]
    base-max = 100
    string-max = 50
    collection-max = 100

    [types]
    base = "any"
    charset = "ascii"
    include = ["int", "float", "string", "boolean", "null", "array", "object"]
    ```

=== "API"

    ```py
    import oddsprout

    oddsprout.Config(
        base_size=(0, 100),
        string_size=(0, 50),
        collection_size=(0, 100),
        base="any",
        charset="ascii",
        types=["int", "float", "string", "boolean", "null", "array", "object"]
    )
    ```

## Settings

### `base`
The type to use for the JSON's root. Valid options are `"any"`, `"array"`, and
`"object"`. Choosing `"any"` will randomly select the base type. 

Defaults to `"any"`.

### `charset`
The set of characters to use for string generation. Valid options are:

* `"ascii"`: all characters from `0x00` to `0x7F`
* `"alpha"`: `A–Z` and `a–z`
* `"alnum"`: `"alpha"` + `0–9`
* `"digits"`: `0–9`

Defaults to `"ascii"`.

### Bounds
Three types of bounds can be specified:

* **base** bounds dictate the size of the root collection
* **string** bounds dictate the length of generated strings
* **collection** bounds dictate the size of nested collections

In the Python API, they are specified through the `base_size`, `string_size`,
and `collection_size` parameters, all of which are of type `tuple[int, int]`
(specifying the minimum and maximum size).

In the CLI TOML configuration, the bounds can be specified through `base`,
`string`, and `collection` settings, all of which require an array of 2
integers. Alternatively, by suffixing the setting with `-max`, you can only set
the maximum value, making e.g. `string-max = 30` equivalent to
`string = [0, 30]`.

=== "Range settings"

    ```toml
    base = [0, 20]
    string = [0, 30]
    collection = [0, 10]
    ```

=== "`-max` settings"

    ```toml
    base-max = 20
    string-max = 30
    collection-max = 10
    ```

!!! warning
    Oddsprout heavily relies on recursion to generate JSONs, which means it may
    fail for more extreme `bounds` configurations. For the Python API, you can
    attempt to counter this by [increasing the recursion limit][sys-recursion].

### Types
The data types to include during generation. Defaults to using all types.
In the Python API, they're specified via the `types` parameter, which is a
`tuple[str, ...]`. In the CLI, they're specified via the `include` or `exclude`
setting, both of which are arrays of type names. Duplicate types are ignored.

**Example:** Only generate arrays of numbers, booleans, and nested arrays:

=== "Python API"

    ```py
    import oddsprout

    oddsprout.JSONGenerator(
        oddsprout.Config(base="array", types=("number", "boolean", "array"))
    )
    ```

=== "TOML (using `include`)"

    ```toml
    [types]
    base = "array"
    include = ["number", "boolean", "array"]
    ```

=== "TOML (using `exclude`)"

    ```toml
    [types]
    base = "array"
    exclude = ["string", "object", "null"]
    ```

!!! tip
    The `"number"` type is an alias for including `"int"` and `"float"` at once.
    The above example would behave the same way if
    `Config(..., types=("int", "float", "boolean", "array"))` or
    `include = ["int", "float", "boolean", "array"]` were supplied.

[sys-recursion]: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit