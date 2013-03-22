import sys
import yaml
import unittest

# Load Module
sys.path.append('../src')
import cobbler_puppet

class CustomExceptionsTests(unittest.TestCase):


    def testEncParameterNotFound(self):
        print "\nTesting EncParameterNotFound Exception..."
        try:
            raise cobbler_puppet.EncParameterNotFound("Test")
        except cobbler_puppet.EncParameterNotFound:
            pass
        else:
            self.fail("Raised exception not thrown.")


    def testInvalidSystemDefinition(self):
        print "\nTesting InvalidSystemDefinition Exception..."
        try:
            raise cobbler_puppet.InvalidSystemDefinition("Test")
        except cobbler_puppet.InvalidSystemDefinition:
            pass
        else:
            self.fail("Raised exception not thrown.")

if __name__ == "__main__":
    unittest.main()

