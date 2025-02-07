# Brainfuck Interpreter

## Installation

This is my [Brainfuck](https://esolangs.org/wiki/Brainfuck) interpreter, one of the most famous esoteric programming languages, written in Python.

To run this project, you might need to install [uv](https://github.com/astral-sh/uv) (a fast alternative to pip).
If you don’t have it yet, install it with:

```sh
pip install uv
```

## Usage

To run the Brainfuck interpreter, use:

```sh
uv run interpreter.py -f your_program.bf
```

To convert the input to text, use:

```sh
uv run interpreter.py -c -f your_program.bf
```

or

```sh
uv run interpreter.py --char --file your_program.bf
```

The instruction stack size defaults to 2**16. To adjust it, use:

```sh
uv run interpreter.py -s 128 -f your_program.bf
```

or

```sh
uv run interpreter.py --stack-size 128 --file your_program.bf
```

## Running Tests

To launch unit tests, run:

```sh
uv run pytest interpreter.py
```

## Example

```sh
uv run interpreter.py -c -f hello_world.bf

$ Hello World!
```
