# ProfileFox

A Tk GUI to help run and kill Firefox profiles. Also enable directing opened links to the profile you want on a link by link basis.

## Current state:

* Runs on windows. has to be placed together with Firefox.exe
* Cross platform where code is not windows specific
* Can receive a URL and forward it to a specific profile so can replace the browser in *xdg-open*

## TODO:

* Make the project fully cross platform by refactoring the OS specific commands/actions to an import or function dictionary or whatever
* Enable scrolling the list of profiles when the list gets too long (currently adds columns instead)

## Dragons

Clones and renames the Firefox executable to differentiate between the profile specific processes on windows. On Linux the information can be gleaned from the process' command line arguments.
