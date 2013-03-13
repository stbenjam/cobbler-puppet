
import sys
import yaml
import unittest

# Load Module
sys.path.append('..')
import cobbler_puppet

class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.config = cobbler_puppet.Config(configFile="data/test.conf")

    def testConfig(self):
        self.assertEqual(self.config.username, "cobbler")
        self.assertEqual(self.config.password, "password")
        self.assertEqual(self.config.api_url, "http://localhost/cobbler_api")
        self.assertEqual(self.config.external_nodes, "/bin/cat")
        self.assertEqual(self.config.node_lister,"/bin/cat")

if __name__ == "__main__":
    unittest.main()

