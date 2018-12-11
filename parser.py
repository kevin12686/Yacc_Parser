import sys
import re


class Arithmetic(object):
    operator_reguler = re.compile(r'^[\+\-\*\/\(\)]')
    integer_reguler = re.compile(r'^-?\d+')
    spacial_reguler = re.compile(r'(^\-\(|(?<=[\+\-\*\/])\-\()')
    spacial_replacement = '-1*('
    operator_weight = {'+': 0, '-': 0, '*': 1, '/': 1, '(': 99}

    def __init__(self, input_string):
        self.input_string = input_string
        self.token_list = Arithmetic._scanner(self.input_string)
        self.postfix_list = Arithmetic._postfix(self.token_list)
        self.final_answer = Arithmetic._calculate(self.postfix_list)

    def __repr__(self):
        return '{}={}'.format(self.input_string, self.final_answer)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def _scanner(input_string):
        is_num = False
        token_list = list()
        input_string = Arithmetic.spacial_reguler.sub(Arithmetic.spacial_replacement, input_string)
        while len(input_string) > 0:
            operator_match = Arithmetic.operator_reguler.match(input_string)
            integer_match = Arithmetic.integer_reguler.match(input_string)
            if is_num or not integer_match:
                is_num = False
                operator_match = operator_match.group(0)
                token_list.append(operator_match)
                input_string = input_string[len(operator_match):]
            else:
                is_num = True
                integer_match = integer_match.group(0)
                token_list.append(int(integer_match))
                input_string = input_string[len(integer_match):]
        return token_list

    @staticmethod
    def _postfix(token_list):
        stack = list()
        postfix_list = list()
        for token in token_list:
            if isinstance(token, int):
                postfix_list.append(token)
            else:
                if len(stack) > 0:
                    if token == '(':
                        stack.append(token)
                    elif token == ')':
                        stack.reverse()
                        posistion = stack.index('(')
                        postfix_list += stack[:posistion]
                        stack = stack[posistion + 1:]
                        stack.reverse()
                    elif stack[-1] == '(' or Arithmetic.operator_weight[token] >= Arithmetic.operator_weight[stack[-1]]:
                        stack.append(token)
                    else:
                        stack.reverse()
                        postfix_list += stack
                        stack.clear()
                        stack.append(token)
                else:
                    stack.append(token)
        stack.reverse()
        postfix_list += stack
        return postfix_list

    @staticmethod
    def _calculate(postfix_list):
        stack = list()
        for each in postfix_list:
            if isinstance(each, int):
                stack.insert(0, each)
            elif each == '+':
                stack.insert(0, stack.pop(1) + stack.pop(0))
            elif each == '-':
                stack.insert(0, stack.pop(1) - stack.pop(0))
            elif each == '*':
                stack.insert(0, stack.pop(1) * stack.pop(0))
            elif each == '/':
                stack.insert(0, stack.pop(1) / stack.pop(0))
        return stack[0]


if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if filename:
        with open(filename, 'r') as f:
            data = [string.strip() for string in f]
        for each in data:
            try:
                print(Arithmetic(each))
            except:
                print('{} Error'.format(each))
    else:
        print("usage: python {} [file]".format(sys.argv[0]))
