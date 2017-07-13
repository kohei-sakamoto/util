"""
A test tool for code puzzles.
Usage: python cp_tester.py <test subject> <test setting>
Requirement:
  Test subject: Command line executions that take test data as standard input
                and return results as standard output.
  Test setting: JSON files for test data and correct result for the data.
                For dry run, output shoud not be defined.
                JSON scheme is following.
                The inputs and outputs are defined as multiple lines of
                standatd input/output.
                Last newlines are not submitted/expected for inputs/outputs.
                  {
                    data: [
                      input:  [ {string} ],
                      output: [ {string} ] 
                    ]
                  }
  
"""

import sys
import json
import time
import math
from subprocess import Popen, PIPE, STDOUT

argv = sys.argv
argc = len(argv)

def usage():
    """show usage.
    """
    print("usage : {0} <program> <test setting>".format(argv[0]))

def test(cmd, test_case):
    """test cmd with one test_case
      cmd:       name of command for test
      test_case: one test case setting
    """
    input = "\n".join(test_case["input"])

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

    expected = "\n".join(test_case["output"])
    if output == expected:
        print("OK")
    else:
        print("NG : expected")
        print(expected)


if (argc < 3):
    usage()
    exit(-1)

test_file = open(argv[2])
test_data = json.load(test_file)

for i, test_case in enumerate(test_data["data"]):
    print("test case {0}...".format(i))
    test(argv[1], test_case)