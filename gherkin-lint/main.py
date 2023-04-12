import argparse
from gherkinlinter import GherkinLinter


if __name__=="__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("files", nargs="+")
    args = argParser.parse_args()

    linter=GherkinLinter()
    linter.lint(args.files)
