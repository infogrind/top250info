#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import re

# Global options with default values.
verbose = False
output = "-"
configfile = "top250info.cfg"
moviefile = "top250.txt"
moviedir = None
showpresent = False
showmissing = False
fuzzy = False

# Minimal and maximal fuzzy match score to count as "approximate" match
# See documentation at https://github.com/seatgeek/fuzzywuzzy
fuzzymin = 80
fuzzymax = 99


def main():
    args = parse_options(sys.argv[1:])
    if verbose:
        debugPrintConfig()
    verifyConfiguration()

    movies = cleanMovieNames(moviesFromFile(moviefile))
    dirs = subdirsOfMovieDir(moviedir)

    if fuzzy:
        showApproximateMatches(dirs, movies)
    else:
        processMoviesNormally(dirs, movies)

def processMoviesNormally(dirs, movies):
    checked = checkMovies(movies, dirs)
    present = {k: v for k, v in checked.items() if v}
    missing = {k: v for k, v in checked.items() if not v}

    if showpresent or (not showpresent and not showmissing):
        print "Locally present Top 250 movies:"
        for m in sorted(present):
            print "- %s" % m
        print

    if showmissing or (not showpresent and not showmissing):
        print "Locally missing Top 250 movies:"
        for m in sorted(missing):
            print "- %s" % m

def showApproximateMatches(dirs, movies):
    import fuzzywuzzy.process
    import fuzzywuzzy.fuzz

    print "Approximate title matches:"
    choices = dirs.keys()
    for m in movies:
        result = fuzzywuzzy.process.extractOne(m, choices,
                scorer=fuzzywuzzy.fuzz.token_sort_ratio)
        if result is None:
            continue
        (name, score) = result
        if score >= fuzzymin and score <= fuzzymax:
            print("- %s" % m)
            print("  Match(%d): %s" % (score, name))

    print ""

def cleanMovieNames(movies):
    def cleanMovieName(title):
        title = re.sub(r" *: *", " - ", title)
        return title
    return map(cleanMovieName, movies)

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
        dirs[d] = True

    debug("Found %d movie subdirectories" % len(dirs))
    return dirs
    

def moviesFromFile(moviefile):
    with open(moviefile) as f:
        movies = [x.strip() for x in f.readlines()]
        return movies

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
  -m        Display the list of missing movies.
  -p        Display the list of present movies.
            By default, both lists are shown. But if you explicitly specify only
            -m or -p, then the respective other list is not shown.
  -z        Use fuzzy comparison to list approximate matches. This is useful if
            you consider renaming your movies locally, or to add additional
            rules for movie name cleanup. (This option requires the fuzzywuzzy
            module to be available). With this option set, the program displays
            those local movies that are a close, but not exact match to the top
            250 list. (If this is set, the -m and -p options have no effect.)
  -h        Show this help text.
  -v        Display verbose output.
  -o <file> Write output to <file> or to stdout if <file> is '-'.
  """


def parse_options(args):

    # Access global variables
    global verbose, output, moviefile, moviedir, showpresent, showmissing
    global fuzzy

    # Parse options using Getopt; display an error and exit if options could
    # not be parsed.
    try:
        opts, args = getopt.getopt(args, "o:hvd:f:pmz")
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
        elif opt == "-p":
            showpresent = True
        elif opt == "-m":
            showmissing = True
        elif opt == "-z":
            fuzzy = True
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

