import argparse
import re

import pytest

#################################################
#               IMPLEMENTATION                  #
#################################################


class Brainfuck:
    def __init__(
        self,
        instruction: str,
        print_output: bool = False,
        print_stack: bool = False,
        stack_size: int = 2**16,
    ) -> None:
        self.instruction = instruction
        self.print_output = print_output
        self.print_stack = print_stack
        self.stack_size = stack_size

        self.stack = [0]
        self.output = []
        self.already_interpreted = False

    def _remove_spaces(self) -> str:
        pat = re.compile(r'\s+')
        return pat.sub('', self.instruction)

    def _interpret(self) -> None:
        instruction = self._remove_spaces()
        if not self._is_executable():
            raise ValueError('Some brackets are not closed.')

        stack = [0]
        data_ptr = 0
        inst_ptr = 0

        while inst_ptr < len(instruction):
            match instruction[inst_ptr]:
                case '>':
                    if data_ptr == len(stack) - 1:
                        stack.append(0)
                    data_ptr += 1
                    inst_ptr += 1

                case '<':
                    if not data_ptr == 0:
                        data_ptr -= 1
                    inst_ptr += 1

                case '+':
                    if self.print_stack:
                        print(stack)
                    stack[data_ptr] += 1
                    inst_ptr += 1

                case '-':
                    if self.print_stack:
                        print(stack)
                    if stack[data_ptr] > 0:
                        stack[data_ptr] -= 1
                    inst_ptr += 1

                case '[':
                    if stack[data_ptr] == 0:
                        loop_depth = 1
                        while loop_depth > 0:
                            if loop_depth >= self.stack_size:
                                raise ValueError(
                                    'Stack size not big enough. Be sure to have a large enough stack_size (default=2**16).'
                                )
                            inst_ptr += 1
                            if instruction[inst_ptr] == '[':
                                loop_depth += 1
                            elif instruction[inst_ptr] == ']':
                                loop_depth -= 1
                    inst_ptr += 1

                case ']':
                    loop_depth = 1
                    while loop_depth > 0:
                        inst_ptr -= 1
                        if instruction[inst_ptr] == ']':
                            loop_depth += 1
                        elif instruction[inst_ptr] == '[':
                            loop_depth -= 1

                case '.':
                    if self.print_output:
                        print(stack[data_ptr])
                    self.output.append(stack[data_ptr])
                    inst_ptr += 1

                case ',':
                    while True:
                        char = input('input an int: ')
                        try:
                            stack[data_ptr] = int(char)
                            break
                        except ValueError:
                            print('Invalid input, be sure to choose an int')
                    inst_ptr += 1
        self.stack = stack
        self.already_interpreted = True

    def _is_executable(self) -> bool:
        count_bracket = 0
        for c in self.instruction:
            if c == '[':
                count_bracket += 1
            elif c == ']':
                count_bracket -= 1
        return count_bracket == 0

    def interpret(self) -> list[int]:
        if not self.already_interpreted:
            self._interpret()
        return self.output

    def interpret_to_char(self) -> str:
        if not self.already_interpreted:
            self._interpret()
        chars = [chr(n) for n in self.output]
        return ''.join(chars)


#################################################
#                 EXECUTION                     #
#################################################


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True)
    parser.add_argument('--char', '-c', action=argparse.BooleanOptionalAction)
    parser.add_argument('--stack-size', '-s', type=int, default=2**16, required=False)

    args = parser.parse_args()

    with open(args.file, 'r') as file:
        instruction = file.read()

        bf = Brainfuck(instruction, stack_size=args.stack_size)

        if args.char:
            print(bf.interpret_to_char())
        else:
            print(bf.interpret())


if __name__ == '__main__':
    main()


#################################################
#                    TESTS                      #
#################################################


@pytest.fixture
def simple_instruction() -> str:
    instruction = """
        ++ > +++++
        [
            < + > -
        ]
        ++++ ++++
        [
            < +++ +++ > -
        ]
        < .
    """
    return instruction


@pytest.fixture
def hello_world_instruction() -> str:
    instruction = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
    return instruction


@pytest.fixture
def open_bracket_instruction() -> str:
    instruction = '++++[>+<->.'
    return instruction


def test_remove_spaces(simple_instruction) -> None:
    bf_simple = Brainfuck(simple_instruction)

    assert bf_simple._remove_spaces() == '++>+++++[<+>-]++++++++[<++++++>-]<.'


def test_interpret(simple_instruction, hello_world_instruction) -> None:
    bf_simple = Brainfuck(simple_instruction)
    bf_hello = Brainfuck(hello_world_instruction)

    assert bf_simple.interpret() == [55]
    assert bf_hello.interpret() == [
        72,
        101,
        108,
        108,
        111,
        32,
        87,
        111,
        114,
        108,
        100,
        33,
        10,
    ]


def test_interpret_to_char(simple_instruction, hello_world_instruction) -> None:
    bf_simple = Brainfuck(simple_instruction)
    bf_hello = Brainfuck(hello_world_instruction)

    assert bf_simple.interpret_to_char() == '7'
    assert bf_hello.interpret_to_char() == 'Hello World!\n'


def test_is_executable(open_bracket_instruction) -> None:
    bf_open = Brainfuck(open_bracket_instruction)

    with pytest.raises(ValueError) as e_info:
        bf_open.interpret()
    assert e_info.value.args[0] == 'Some brackets are not closed.'


def test_stack_size(hello_world_instruction) -> None:
    bf_hello = Brainfuck(hello_world_instruction, stack_size=2)

    with pytest.raises(ValueError) as e_info:
        bf_hello.interpret()
    assert (
        e_info.value.args[0]
        == 'Stack size not big enough. Be sure to have a large enough stack_size (default=2**16).'
    )
