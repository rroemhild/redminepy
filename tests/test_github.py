#!/usr/bin/env python
from eukalypse_brew import Github
import unittest


class MyGithubTest(unittest.TestCase):

    def setUp(self):
        self.github = Github("rroemhild", "redminepy")

    def test_check_readme(self):
        self.github.check_readme()
