from typing import Iterator, Sequence
import os
from gherkin.parser import Parser
from gherkin.errors import CompositeParserException
from rules.use_and import run


class GherkinLinter():
    parser = Parser()

    def _parse_file(self, file: str) -> dict | CompositeParserException:
        with open(file, "r", encoding="utf8") as content:
            try:
                return self.parser.parse(content.read())
            except CompositeParserException as e:
                return e

    def _discover_files(self, paths: Sequence[str]) -> Iterator[str]:
        for path in paths:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    yield from (
                        os.path.join(root, file)
                        for file in files
                        if file.endswith(".feature")
                    )
            elif os.path.isfile(path) and path.endswith(".feature"):
                yield path

    def lint(self, paths: Sequence[str]) -> None:
        errors = []
        for file in self._discover_files(paths):
            file_errors = []
            parse_result = self._parse_file(file)
            if isinstance(parse_result, CompositeParserException):
                file_errors = parse_result.errors
            elif isinstance(parse_result, dict):
                file_errors = run(parse_result["feature"])
            errors.append(
                {"file": os.path.normpath(file), "errors": file_errors})
        # Output errors or perform other actions as needed
        print(errors)
