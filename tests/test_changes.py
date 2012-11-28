import os
import unittest

SCRIPT_PATH = os.path.dirname(__file__)

from reprepro.changes import Changes

class ChangesTestCase(unittest.TestCase):
    def setUp(self):
        changes_path = os.path.join(SCRIPT_PATH, 'files', 'sample.changes')

        self.changes = Changes(changes_path)

    def test_distribution(self):
        self.assertEquals('lucid', self.changes['Distribution'])

    def test_files(self):
        expected = sorted(['rubygems-appscale_1.3.7-2.dsc', 'rubygems-appscale_1.3.7-2.diff.gz', 'rubygems-appscale_1.3.7-2_amd64.deb'])
        actual = sorted([str(x) for x in self.changes.files])

        self.assertEquals(expected, actual)
