import re
import pytest

class Brainfuck:
    def __init__(self, instruction: str, print_stack: bool = False) -> None :
        self.instruction = instruction
        self.print_stack = print_stack
        self.stack = [0]
        self.output = []
        self.already_interpreted = False


    def _remove_spaces(self) -> str :
        pat = re.compile(r'\s+')
        return pat.sub('', self.instruction)


    def _interpret(self) -> None :
        instruction = self._remove_spaces()

        stack = [0]
        data_ptr = 0
        inst_ptr = 0

        while inst_ptr < len(instruction):

            match instruction[inst_ptr]:
                case ">":
                    if data_ptr == len(stack) - 1:
                        stack.append(0)
                    data_ptr += 1
                    inst_ptr += 1

                case "<":
                    if not data_ptr == 0:
                        data_ptr -= 1
                    inst_ptr += 1

                case "+":
                    stack[data_ptr] += 1
                    inst_ptr += 1

                case "-":
                    if stack[data_ptr] > 0:
                        stack[data_ptr] -= 1
                    inst_ptr += 1

                case "[":
                    if stack[data_ptr] == 0:
                        loop_depth = 1
                        while loop_depth > 0:
                            inst_ptr += 1
                            if instruction[inst_ptr] == "[":
                                loop_depth += 1
                            elif instruction[inst_ptr] == "]":
                                loop_depth -= 1
                    inst_ptr += 1

                case "]":
                    loop_depth = 1
                    while loop_depth > 0:
                        inst_ptr -= 1
                        if instruction[inst_ptr] == "]":
                            loop_depth += 1
                        elif instruction[inst_ptr] == "[":
                            loop_depth -= 1

                case ".":
                    if self.print_stack:
                        print(stack[data_ptr])
                    self.output.append(stack[data_ptr])
                    inst_ptr += 1

                case ",":
                    while True:
                        char = input("input char/int: ")
                        try:
                            stack[data_ptr] = int(char)
                            break
                        except ValueError:
                            print("Invalid character/int")
                    inst_ptr += 1
        self.stack = stack
        self.already_interpreted = True


    def interpret(self) -> list[int]:
        if not self.already_interpreted:
            self._interpret()
        return self.stack


    def interpret_to_char(self) -> str:
        if not self.already_interpreted:
            self._interpret()
        chars = [chr(n) for n in self.output]
        return "".join(chars)




def main():
    # TODO: check code for non closed loop
    instruction = input("Enter your instruction: ")

    bf = Brainfuck(instruction)
    chars = bf.interpret_to_char()
    print(bf.interpret())
    print(chars)
    

if __name__ == "__main__":
    main()

