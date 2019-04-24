This was my first Python project and possibly even my first public
release.
----

I urge you to use python's builtin [argparse module](https://docs.python.org/3/library/argparse.html).


clargs
===

clargs is a simple function that tries to provide a simple, yet flexible
and attractive way to handle parsing of command line arguments.


## Features

* Explicit type conversion. Default type is *string*
* Support for default values
* Supports long and shorthand argument names
* Returns a dictionary including another dictionary 'named' for named arguments (structured as  `argument name -> value` as `k -> v`) and a list 'rogue' for unnamed arguments

## Command-line Usage
* Strings, Integers and other types
	* Complete: `--output=/dev/null` **or** `--repetitions=10`
	* Shorthand: `-o /dev/null` **or** `-o/dev/null` **or** `-r10` **or** `-r 10`
* Booleans
	* Complete: `--verbose` for True **or** `--noverbose` for False
	* Shorthand: `-v` for True **or** `-V` for False

## Script Usage
The package clargs exposes one function that takes two parameters, `parse`.

The first parameter, `argument format` is a *dictionary*. It defines the way you want your arguments to be parsed. Its structure is as follows:
`argument`: `format`, where  `argument` is a *string* and `format` is a *tuple* of length *0*, *1*, *2* or *3*.

The first element of the tuple should represent the single-character shorthand version of the argument, with the second being the default value and the third element representing the requested type that the argument will be explicitly converted to.

## Example
#### `python example.py -v -o hello.txt -r10`
```python
import sys
import clargs


def main(args):
    with open(args['named']['output'], 'w') as f:
        if args['named']['verbose']:
            print("Successfully opened file for writing!")

        for i in range(args['named']['repetitions']):
            f.write("Hello there, #%d!\n" % (i+1))

if __name__ == "__main__":
    argformat = {
        "output": ("o", "output.txt"),
        "verbose": ("v", False, bool),
        "repetitions": ("r", 3, int),
        "somethingelse": (),
    }

    argv = sys.argv[1:]

    args = clargs.parse(argformat, argv)
    main(args)

```
