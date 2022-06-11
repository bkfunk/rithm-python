from dataclasses import dataclass
from typing import List, Sequence, Tuple
from rich.pretty import pretty_repr
import re


@dataclass
class StringStandardizer:
    indent_str: str = 4 * " "
    breakers: Tuple[str] = ","
    openers: Tuple[str] = ("(", "[", "{")
    closers: Tuple[str] = (")", "]", "}")

    def get_lines(self, string: str) -> List[str]:
        result = []
        current = ""
        for char in string:
            if char in self.openers or char in self.breakers:
                result.append(current + char)
                current = ""
            elif char in self.closers:
                result.append(current)
                current = char
            else:
                current += char

        # Add last line
        if len(current) > 0:
            result.append(current)
        return result

    def indent_lines(self, lines: List[str]) -> List[str]:
        result = []
        indent = 0

        def append_line(line):
            result.append(indent * self.indent_str + line)

        for line in lines:
            if line.endswith(self.openers):
                append_line(line)
                indent += 1
            elif line.startswith(self.closers):
                indent -= 1
                append_line(line)
            else:
                append_line(line)
        return result

    def indent(self, string) -> str:
        lines = self.get_lines(string)
        return "\n".join(self.indent_lines(lines))


def std_str(string) -> str:
    string = string.replace("'", '"')

    string = re.sub(r"\s+", "", string)

    stdizer = StringStandardizer()
    return stdizer.indent(string)
    # lines = [
    #     " ".join([tok for tok in line.strip().split(" ")])
    #     for line in str(string).split("\n")
    #     if len(line.strip()) > 0
    # ]

    # return "".join(lines).replace("(", "(\n").replace(")", "\n)")


# class TestRepr:
#     def __init__(self, arg):
#         self.arg = arg


#     def __repr__(self) -> str:
#         return pretty_repr(self.arg)

#     def __str__(self) -> str:
#         return pretty_repr(self.arg)

#     def __eq__(self, other) -> bool:
#         if isinstance(other, TestRepr):
#             return self.arg == other.arg

#         if isinstance(other, str):
#             return std_str(self) == std_str(other)
