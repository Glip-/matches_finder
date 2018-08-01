import unittest
import sys
sys.path.append('..')

import matchesFinder


class TestMatchesFinder(unittest.TestCase):
    def test_without_required_args(self):
        """
        User didn't pass all required args
        """
        self.parser = matchesFinder.parse_arguments()
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-r', 'rrr'])
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['-f', 'fff'])

    def test_cannot_open_file(self):
        """
        User passed wrong name of text file
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', 'abcd', '-f', 'wrong'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(self.m.output, None)

    def test_no_matches_in_a_file(self):
        """
        Can't find any matches in the file
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', 'abcd', '-f', 'file1'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(self.m.output, [])

    def test_found_matches_normal_output__one_file(self):
        """
        Found matches and print text
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', '[S,s]witch', '-f', 'file1'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(len(self.m.output), 3)

    def test_found_matches_color_output__two_files(self):
        """
        Found matches and colored text
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', '[S,s]witch', '-f', 'file1,file2', '-c'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(len(self.m.output), 4)
        self.assertIn("32m", self.m.op.coloredText)

    def test_found_matches_underscore_output__two_files(self):
        """
        Found matches in two files and underscored it
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', '[S,s]witch', '-f', 'file1,file2', '-u'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(len(self.m.output), 4)
        self.assertIn("^", self.m.op.underscoreText)

    def test_found_matches_machine_readable_output__one_file(self):
        """
        Found matches and create machine readable output
        """
        self.parser = matchesFinder.parse_arguments()
        self.args = self.parser.parse_args(['-r', '[S,s]witch', '-f', 'file2', '-m'])
        self.m = matchesFinder.matchesFinder(self.args)
        self.assertEqual(len(self.m.output), 4)
        self.assertEqual(len(self.m.op.outputText.split(":")), 7)


if __name__ == '__main__':
    unittest.main()
