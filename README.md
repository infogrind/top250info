# IMDb Top 250 Movie Checker

The goal of this program is to tell you which of [IMDb's top 250
movies](https://www.imdb.com/chart/top) you already have locally, and which ones
are missing. The program does this by comparing the list of movies in a given
text file (normally `top250.txt`) with the subdirectories of a specified
directory. The assumption is that if a given movie exists locally, then a
subdirectory exists with the same name as the entry in the text file.

## Usage:

The script has its own usage instructions:

```
python top250info.py -h
```
