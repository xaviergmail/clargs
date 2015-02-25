import re
import sys


full_re = r'^--(no)?([\w|-]*)(=(.*))?$'
short_re = r'^-(\w)(\w*)?$'
upper_re = r'^[a-z]*$'


def parse(argformat, argv):
    # Initialize rogue list and named dict
    rogue = []
    named = {}

    argc = len(argv)

    i = 0
    while i < argc:
        # Current argument value in the loop
        arg = argv[i]

        # Search for the abbreviated options first
        short = re.match(short_re, arg, re.I)
        full = None

        # Search for the full option if shorthand wasn't found
        if not short:
            # Search for the full argument
            full = re.match(full_re, arg, re.I)

            # Still haven't found a match. Add to rogue list and continue
            if not full:
                rogue.append(arg)
                i += 1
                continue

        # Loop through argument data to find desired type. Default to str
        for arg, argd in argformat.items():
            argType = argd[2] if len(argd) > 2 else str

            # Shorthand match!
            if short and short.group(1).lower() == argd[0]:

                # Boolean requested! True if lowercase, False if UPPERCASE
                if argType is bool:
                    named[arg] = re.search(upper_re, short.group(1))

                # 'Compressed' argument, Ex: -oSomething
                # Take the value from the second capture group
                elif short.group(2):
                    named[arg] = short.group(2)

                # Our value is stored in the next index.
                # Error out with missing argument if we go out of range
                else:
                    if i + 2 > argc:
                        sys.stderr.write(
                            "Error: Missing value for argument %s\n" %
                            short.group(1))
                        sys.exit(1)

                    i += 1

                    # Store the value in the index
                    named[arg] = argv[i]
                # Successfully matched a shorthand argument! Break out of loop.
                break

            # Full name match!
            elif full and full.group(2).lower() == arg:
                # Boolean requested. Assign the inverse of capture group 1 (no)
                if argType is bool:
                    named[arg] = not bool(full.group(1))

                # Equal sign found, assign value found after it
                elif full.group(4):
                    named[arg] = full.group(4)
                break  # Success, exit this inner loop

        else:  # Did not break out of the loop, error out.
            sys.stderr.write("Error: Unknown argument %s\n" %
                            ("-" + short.group(1) if short else
                             "--" + full.group(1)))
            sys.exit(1)

        i += 1

    for arg, argd in argformat.items():
        # Default argument, if specified
        if not arg in named and len(argd) > 1:
            named[arg] = argd[1]

        # Convert to the requested type, if specified. This will also convert
        # the previously assigned regex/group matches to booleans.
        elif len(argd) > 2:
            named[arg] = argd[2](named[arg])

    ret = {}
    ret["named"] = named
    ret["rogue"] = rogue

    return ret
