#!/usr/bin/python

# Complain with: Reynaldo Baquerizo <reynaldomic@gmail.com>
# Thu 07 Oct 2010 02:43:11 PM PET

"""
My take on a calculator with reverse polish notation
See http://en.wikipedia.org/wiki/Reverse_Polish_notation
"""
import sys
import pdb
import operator as op

operations = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.div
}

def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if callable(token):
            stack.insert(0, token(stack.pop(1), stack.pop(0)))
        elif isinstance(token, float):
            stack.insert(0, token)
    return stack.pop()

def parse_rpn(line):
    return [operations[x] if x in operations else float(x) for x in
            line.split()]

def rpn(line):
    return eval_rpn(parse_rpn(line))

def test_rpn():
    assert rpn("4 3 + 9 3 / *") == 21
    assert rpn("7.2 1.6 +") == 8.8
    assert rpn("10 3 /") == float(10) / 3
    assert rpn("2 -3 + 1 9 / 6 7 * * +") == -1 + (1.0 / 9) * (6 * 7)
    assert rpn("-4 1 -") == -5

if __name__ == "__main__":
    test_rpn()
