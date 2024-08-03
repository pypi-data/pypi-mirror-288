import unittest
import sys

pattern = "*_test.py"

if len(sys.argv) > 1:
    pattern = sys.argv[1]

loader = unittest.TestLoader( )
suite = loader.discover('pbftests', pattern=pattern)
unittest.TextTestRunner( ).run(suite)

