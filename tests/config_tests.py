
import sys
import yaml
import unittest

# Load Module
sys.path.append('../src')
import cobbler_puppet

class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.config = cobbler_puppet.Config(configFile="data/test.conf")

    def testConfig(self):
        print "Testing Config Class..."
        self.assertEqual(self.config.username, "cobbler", "Username mismatch")
        self.assertEqual(self.config.password, "password", "Password mismatch")
        self.assertEqual(self.config.api_url, "http://localhost/cobbler_api", "API URL Mismatch")
        self.assertEqual(self.config.external_nodes, "/bin/cat", "external_nodes mismatch")
        self.assertEqual(self.config.node_lister,"/bin/cat", "node_lister mismatch")

if __name__ == "__main__":
    unittest.main()

