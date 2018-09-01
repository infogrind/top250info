#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
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
    verifyConfiguration()

    movies = moviesFromFile(moviefile)
    dirs = subdirsOfMovieDir(moviedir)
    checked = checkMovies(movies, dirs)
    present = {k: v for k, v in checked.items() if v}
    missing = {k: v for k, v in checked.items() if not v}

    print "Locally prsent Top 250 movies:"
    for m in sorted(present):
        print "- %s" % m

    print
    print "Locally missing Top 250 movies:"
    for m in sorted(missing):
        print "- %s" % m

def checkMovies(movies, dirs):
    checked = {}
    for m in movies:
        if m in dirs:
            debug("Found movie %s locally" % m)
            checked[m] = True
        else:
            debug("Did NOT found movie %s locally" % m)
            checked[m] = False
    return checked

def subdirsOfMovieDir(moviedir):
    dirs = {}
    for d in os.listdir(moviedir):
        debug("Entry of movie directory: %s" % d)
        if os.path.isdir(os.path.join(moviedir, d)):
            debug("It is a directory")
            dirs[d] = True
        else:
            debug("It is not a directory")

    debug("Found %d movie subdirectories" % len(dirs))
    return dirs
    

def moviesFromFile(moviefile):
    with open(moviefile) as f:
        content = [x.strip() for x in f.readlines()]
        return content

def verifyConfiguration():
    errors = False
    if moviedir is None:
        error("Movie directory not set. See help (-h).")
        errors = True
    elif not os.path.isdir(moviedir):
        error("Movie directory does not exist: %s" % moviedir)
        errors = True
    elif not os.access(moviedir, os.R_OK):
        error("Movie directory is not readable: %s" % moviedir)
        errors = True
    if not os.path.isfile(moviefile):
        error("Movie file does not exist: %s" % moviefile)
        errors = True
    elif not os.access(moviefile, os.R_OK):
        error("Movie file is not readable: %s" % moviefile)
    
    if errors:
        sys.exit(1)


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
  -f <file> Reads the top 250 movies from the given file
            (default value: top250.txt)
  -d <dir>  The directory where the movies are stored locally.
            (mandatory argument)
  -h        Show this help text.
  -v        Display verbose output.
  -o <file> Write output to <file> or to stdout if <file> is '-'.
  """


def parse_options(args):

    # Access global variables
    global verbose, output, moviefile, moviedir

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

def error(s):
    sys.stderr.write("ERROR: %s\n" % s)

def fatal(s):
    sys.stderr.write("FATAL ERROR: %s\n" % s)
    sys.exit(1)

def warning(s):
    sys.stderr.write("WARNING: %s\n" % s)

# This is the most important line: it calls the main function if this program is
# called directly.
if __name__ == "__main__":
    main()

