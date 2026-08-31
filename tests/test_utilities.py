"""Unit tests for Chatbook client helpers."""

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import utilities


class CifrarTests(unittest.TestCase):
    def test_round_trip_ascii(self):
        original = "auth|root|admin"
        self.assertEqual(utilities.cifrar(utilities.cifrar(original)), original)

    def test_key_letter_survives(self):
        original = "auth|Kate|passKword"
        self.assertEqual(utilities.cifrar(utilities.cifrar(original)), original)

    def test_empty(self):
        self.assertEqual(utilities.cifrar(""), "")
        self.assertEqual(utilities.cifrar(None), "")


class SplitNamesTests(unittest.TestCase):
    def test_filters_blanks(self):
        self.assertEqual(utilities.split_names("root|user1||asti|"), ["root", "user1", "asti"])

    def test_empty(self):
        self.assertEqual(utilities.split_names(""), [])
        self.assertEqual(utilities.split_names(" "), [])


class FormatChatTests(unittest.TestCase):
    def test_empty_state(self):
        html = utilities.format_chat_html("", "root")
        self.assertIn("No messages yet", html)

    def test_own_message_marked(self):
        html = utilities.format_chat_html("root->hello\nasti->hi", "root")
        self.assertIn("hello", html)
        self.assertIn('bgcolor="#5b5ce2"', html)
        self.assertIn("asti", html)

    def test_escapes_html(self):
        html = utilities.format_chat_html("root-><script>alert(1)</script>", "root")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


if __name__ == "__main__":
    unittest.main()
