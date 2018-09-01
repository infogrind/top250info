#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt

# Global options with default values.
verbose = False
output = "-"
configfile = "top250info.cfg"
moviefile = "top250.txt"
moviedir = None


def main():
    args = parse_options(sys.argv[1:])
    if verbose:
        debugPrintConfig()



def debugPrintConfig():
    debug("Debug mode enabled.")
    debug("Configuration:")
    debug("- verbose = %s" % verbose)
    debug("- output = %s" % output)
    debug("- moviefile = %s" % moviefile)
    debug("- moviedir = %s" % moviedir)

def usage():
    print """Usage: top250info

Checks which of IMDb's top 250 movies are present in a given local directory.
The program reads the top 250 movies from a text file.  The assumption is that
if a movie is present, the directory name of the movie is the same as the movie
in the file.

The program then summarizes which movies are missing.

  Options:
  -h        Show this help text.
  -v        Display verbose output.
  -o <file> Write output to <file> or to stdout if <file> is '-'.
  -f <file> Reads the top 250 movies from the given file
            (default value: top250.txt)
  -d <dir>  The directory where the movies are stored locally.
            (mandatory argument)
  """


def parse_options(args):

    # Access global variables
    global verbose, output

    # Parse options using Getopt; display an error and exit if options could
    # not be parsed.
    try:
        opts, args = getopt.getopt(args, "o:hvd:f:")
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    # Set variables according to options
    for opt, val in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt == "-v":
            verbose = True
        elif opt == "-o":
            output = val
        elif opt == "-f":
            moviefile = val
        elif opt == "-d":
            moviedir = val
        else:
            assert False, "unhandled option"

    return args


def debug(s):
    if verbose:
        sys.stderr.write(s + "\n")


# This is the most important line: it calls the main function if this program is
# called directly.
if __name__ == "__main__":
    main()

