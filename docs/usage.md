Oddsprout can be used both as a CLI application and as a Python library.

## CLI
Oddsprout can be invoked by the `oddsprout` command (if that doesn't work, try
invoking it via Python, i.e. `python -m oddsprout` if you installed with `pip`).
```console
$ oddsprout --help
usage: oddsprout [-h] [--config CONFIG]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  path to configuration file
```
If no arguments are provided, oddsprout will generate a JSON using the
[default config] and print it to standard output:
```console
$ oddsprout
{
  ">@y3{QR\u000eBU\t\u0006<$\f\u0001\u0014R\u000bSq\u0000i": "I/h2\u000fjxCr\u0006\u0013sk\rRA8`\u0015z}\u0018{l\u001aJ\u001c{4T|9)\fP]",
  "C\u000f\u0010q1-d'\u00064cRE`\b\u0005\u0019},x>2\"aL)\u001e\u007fD@M\u0012H\"Tp": 723670.4717504024,
  "\u001b\u0001x@#": -809897.8178375069,

  *snip*

  "j\u0005\u0017\u0015u\u0017\u007f\u0013<w\u0017\u0006!\rRHzFP)_;": -730165.940092089,
  "IPpp|": -20909.71435106476,
  "{8\u0019La\u001f;\\\u0010_D53%e\rdO9\u0000\u0010'N/'\u000f6\u001ft\u0019Hoq0V$3y$": null
}
```
A config file can be provided with the `--config` flag:
```console
$ cat oddsprout.toml
[bounds]
base-max = 10

[types]
base = "array"
include = ["number", "boolean"]
$ oddsprout --config oddsprout.toml
[
  563672.3124703288,
  false,
  902865.0353718256,
  -64548.64624481776,
  446222.7337318931,
  true,
  -280712.10006229405,
  true,
  -856591
]
```
See the [Configuration] section for details.

---

To save the JSON to a file, simply redirect standard output to the destination:
```console
$ oddsprout --config oddsprout.toml > random.json
```

## API

The Python API comprises of the `JSONGenerator` and `Config` classes, the former
being reliant on the latter. Passing no arguments to `JSONGenerator` will make
it use the [default config]:

```py
import oddsprout

gen = oddsprout.JSONGenerator()
print(gen.generate_value())
# {
#   "2.'gu|l\fH \u007f.B\u0017'gcd\u001a@\u000b\u0000": "}\"sNN4[",
#   "xu{g\u0003Y*\u0017\t\u0000;z%\u001eE05\u00033+lR2@a#jrt\u007f-(`\u0014\u0006tEg/\\&": null,
#   "xnm(vO\u0014\bCD\u0000SYc": null,
#
#   *snip*
#
#   "8o&\bmIcsu\u0007\u007fBz_Njo\u0011w<@": -483862,
#   "Vf\r\u0014hSzL\"\u0002\u000f\u00141~^\f]\u000beIL\u0002\u0007\u00139^ZIK`8)!8j\u0006c\u0018r_\u0015M\u0015": "\u001bc\\a\u000e}v`Ju\r\u000enFk\u0007\u0001Z5S[&qt\b)\u0003A(OP}d|_%/H{a\u001c\u0007"
# }
```

!!! info
    `JSONGenerator.generate_value` returns a Python `list` or `dict`, not a JSON
    string like the CLI.

The only argument `JSONGenerator` accepts is a `Config` object:
```py
import oddsprout

gen = oddsprout.JSONGenerator(
  oddsprout.Config(base_size=(0, 10), base="array", types=("number", "boolean"))
)

print(gen.generate_value())
# [51560, -536427.4840101383, False, False, 382182, -510471]
```

See the [Configuration] section and the [API reference] for details on
configuring oddsprout.

[default config]: configuration.md#default-config
[API reference]: api_reference.md
[Configuration]: configuration.md