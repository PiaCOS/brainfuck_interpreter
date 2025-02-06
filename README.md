# Brainfuck Interpreter

## Installation

This is my Brainfuck interpreter, written in Python.

To run this project, you might need to install [uv](https://github.com/astral-sh/uv) (a fast alternative to pip).
If you don’t have it yet, install it with:

```sh
pip install uv
```

## Usage

To run the Brainfuck interpreter, use:

```sh
uv run interpreter.py < your_program.bf
```

Or, if you want to enter code interactively:

```sh
uv run interpreter.py
```

## Running Tests

To launch unit tests, run:

```sh
uv run pytest interpreter.py
```

## Example

```sh
uv run interpreter.py
>>> ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.

$ Hello World!
```
