"""
A test tool for code puzzles.
Usage: python cp_tester.py <test subject> <test setting>
Requirement:
  Test subject: Command line executions that take test data as standard input
                and return results as standard output.
  Test setting: A formatted file for test data. The format is followings.
                As showed in followings, multiple input/output pairs are allowed.
                INPUT
                <test input data 1 for multiple lines>
                OUTPUT
                <test output data 1 for multiple lines>
                INPUT
                <test input data 2 for multiple lines>
                OUTPUT
                <test output data 2 for multiple lines>
 
"""

import sys
import time
import math
from subprocess import Popen, PIPE, STDOUT

argv = sys.argv
argc = len(argv)

def usage():
    """show usage.
    """
    print("usage : {0} <program> <test setting>".format(argv[0]))

def read_test_file(filename):
    test_data    = None
    current_data = None
    init         = False
    for line in open(filename, 'r'):
        if line.rstrip() == "INPUT":
            if not init:
                # first test data
                test_data    = []
                current_data = {}
                init = True
            else:
                # new test data
                if ("input" not in current_data) or ("output" not in current_data):
                    raise ValueError("INPUT or OUTPUT not exists.")
                test_data.append(current_data);
                current_data = {}
            current_data["input"] = ""
        elif line.rstrip() == "OUTPUT":
            if not init:
                raise ValueError("NO INPUT")
            if "output" in current_data:
                raise ValueError("OUTPUT duplicated")
            current_data["output"] = ""
        else:
            if not init:
                raise ValueError("NO INPUT")
            if not "input" in current_data:
                raise ValueError("NO INPUT")

            if not "output" in current_data:
                current_data["input"] += line
            else:
                current_data["output"] += line
    return test_data

def test(cmd, test_case):
    """test cmd with one test_case
      cmd:       name of command for test
      test_case: one test case setting
    """
    input = test_case["input"]

    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    start  = time.time()
    stdout = p.communicate(input = input.encode("utf8"))[0]
    end    = time.time()

    print("input")
    print(input)

    diff   = end - start
    print("process time : {0}".format(math.floor(diff*1000 + 0.5)))

    print("output")
    output = stdout.decode("utf8")
    print(output)
    if "output" not in test_case:
        return;

    expected = test_case["output"]
    if output.rstrip() == expected.rstrip():
        print("OK")
    else:
        print("NG : expected")
        print(expected)


if (argc < 3):
    usage()
    exit(-1)

test_file = argv[2]
test_data = read_test_file(test_file)

for i, test_case in enumerate(test_data):
    print("test case {0}...".format(i))
    test(argv[1], test_case)