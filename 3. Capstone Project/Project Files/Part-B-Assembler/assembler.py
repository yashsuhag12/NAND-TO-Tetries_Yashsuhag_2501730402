#!/usr/bin/env python3
"""Two-pass Hack assembler. Extra feature for K=23 (K % 3 == 2):
warn when a label is declared more than once.
Usage: python assembler.py input.asm [output.hack]
"""
from pathlib import Path
import re
import sys

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    PREDEFINED[f"R{i}"] = i

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][\w.$:]*$")

def clean_lines(path):
    result = []
    for line_no, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        code = raw.split("//", 1)[0].strip()
        if code:
            result.append((line_no, re.sub(r"\s+", "", code)))
    return result

def assemble(source):
    symbols = dict(PREDEFINED)
    instructions = []
    rom_address = 0
    # Pass 1: labels.
    for line_no, line in source:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if not SYMBOL_RE.match(label):
                raise ValueError(f"Line {line_no}: invalid label '{line}'")
            if label in symbols:
                print(f"Warning: Line {line_no}: duplicate label '{label}' (first definition/address retained).")
            else:
                symbols[label] = rom_address
        else:
            instructions.append((line_no, line))
            rom_address += 1

    # Pass 2: A/C instructions and variables.
    next_variable = 16
    machine = []
    for line_no, line in instructions:
        if line.startswith("@"):
            token = line[1:]
            if token.isdigit():
                value = int(token)
            else:
                if not SYMBOL_RE.match(token):
                    raise ValueError(f"Line {line_no}: invalid A-instruction '{line}'")
                if token not in symbols:
                    symbols[token] = next_variable
                    next_variable += 1
                value = symbols[token]
            if not 0 <= value <= 32767:
                raise ValueError(f"Line {line_no}: A-instruction value out of range: {value}")
            machine.append(f"{value:016b}")
        else:
            if line.count(";") > 1 or line.count("=") > 1:
                raise ValueError(f"Line {line_no}: invalid C-instruction '{line}'")
            if "=" in line:
                dest, remainder = line.split("=", 1)
            else:
                dest, remainder = "", line
            if ";" in remainder:
                comp, jump = remainder.split(";", 1)
            else:
                comp, jump = remainder, ""
            if dest not in DEST:
                raise ValueError(f"Line {line_no}: invalid destination '{dest}'")
            if comp not in COMP:
                raise ValueError(f"Line {line_no}: invalid computation '{comp}'")
            if jump not in JUMP:
                raise ValueError(f"Line {line_no}: invalid jump '{jump}'")
            machine.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
    return machine, symbols

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python assembler.py input.asm [output.hack]")
        raise SystemExit(2)
    source_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else source_path.with_suffix(".hack")
    try:
        machine, symbols = assemble(clean_lines(source_path))
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
    output_path.write_text("\n".join(machine) + "\n", encoding="utf-8")
    print(f"Assembled {len(machine)} instructions -> {output_path}")
    print(f"Symbols defined/allocated: {len(symbols)}")
if __name__ == "__main__":
    main()
