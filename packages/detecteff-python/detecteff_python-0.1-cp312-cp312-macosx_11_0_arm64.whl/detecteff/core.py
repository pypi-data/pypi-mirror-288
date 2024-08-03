
from .rust import detecteff
from .rust import print_help, print_version
from argpi import ArgumentDescription, Arguments, FetchType
from os.path import expanduser, expandvars
from sys import exit as leave

class Detecteff:
    def __init__(self, path: str = "", recursive_search: bool = False, formatted_output: bool = False, ignore: list[str] = []):
        # initialize rust lib
        self.core = detecteff.DetecteffRust(path, recursive_search, formatted_output, ignore)
        # class attr
        self.found_already = False

    def duplicates(self, explicit: bool):
        self.core.find_duplicates(explicit)
        self.found_already = True
    
    def delete(self, explicit: bool):
        self.core.delete_duplicates(self.found_already, explicit)

def run():
    # get currently passed arguments
    arguments = Arguments().__capture__()

    # define project arguments
    arguments.__add__(
        "--scan",
        ArgumentDescription()
            .shorthand('-s')
    )
    arguments.__add__(
        "--recursive",
        ArgumentDescription()
            .shorthand('-r')
    )
    arguments.__add__(
        "--formatted",
        ArgumentDescription()
            .shorthand('-fmt')
    )
    arguments.__add__(
        "--help",
        ArgumentDescription()
            .shorthand('-h')
    )
    arguments.__add__(
        "--version",
        ArgumentDescription()
            .shorthand('-v')
    )
    arguments.__add__("--delete", ArgumentDescription().shorthand('-del'))
    arguments.__add__("--ignore", ArgumentDescription().shorthand('-i'))

    # analyse
    arguments.__analyse__()

    if arguments.__there__("--help"):
        print_help()
        leave(0)
    
    if arguments.__there__("--version"):
        print_version()
        leave(0)

    # define base args
    recursive = False
    formatted = False
    delete = False
    ignore = []

    if arguments.__there__("--delete"):
        delete = True
    
    if arguments.__there__("--recursive"):
        recursive = True
    
    if arguments.__there__("--formatted"):
        formatted = True
    
    if arguments.__there__("--ignore"):
        ignore = arguments.__fetch__("--ignore", FetchType.TILL_NEXT)
        if type(ignore) == str:
            ignore = [ignore]
        
        # print(ignore)
    
    if arguments.__there__("--scan"):
        path = arguments.__fetch__("--scan", FetchType.SINGULAR)
        path = expanduser(path)
        path = expandvars(path)

        # initialize app
        app = Detecteff(path=path, recursive_search=recursive, formatted_output=formatted, ignore=ignore)
        app.duplicates(True)

        if arguments.__there__("--delete"):
            app.delete(True)