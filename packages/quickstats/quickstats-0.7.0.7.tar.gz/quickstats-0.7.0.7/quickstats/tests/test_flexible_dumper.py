import unittest
import numpy as np

from quickstats import FlexibleDumper

class TestFlexibleDumper(unittest.TestCase):
    
    def test_default_settings(self):
        data = [1, 2, [[], [{}, {1: 2, "a": 'b'}]], (5, 3), np.arange(100), 'I\nlove\nyou', [dict, any, {1, 2, 3}, '你']]
        expected_output = "- 1\n- 2\n- - []\n  - - {}\n    - 1: 2\n      a: b\n- - 5\n  - 3\n- [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23\n   24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47\n   48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71\n   72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95\n   96 97 98 99]\n- I\n  love\n  you\n- - <class 'dict'>\n  - <built-in function any>\n  - {1, 2, 3}\n  - 你"
        dumper = FlexibleDumper()
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_indent_and_separator_settings(self):
        data = {"key": "value", "list": [1, 2, 3, 5]}
        dumper = FlexibleDumper(item_indent='--> ', list_indent='*-> ', separator=' => ', skip_str='[...]', max_iteration=3)
        expected_output = "key => value\nlist => \n--> *-> 1\n--> *-> 2\n--> *-> 3\n--> [...]"
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_indent_sequence_on_key(self):
        data = {"key": [1, 2, {"nested": "value"}]}
        dumper = FlexibleDumper(indent_sequence_on_key=True)
        expected_output = "key: \n  - 1\n  - 2\n  - nested: value"
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_max_depth(self):
        data = {"a": {"b": {"c": {"d": "e"}}}}
        dumper = FlexibleDumper(max_depth=2)
        expected_output = "a: \n  b: \n    c: \n      ..."
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_max_iteration(self):
        data = [[1, 2, 3, 4, 5], {1:2, 3:4, 5:6, 7:8}]
        dumper = FlexibleDumper(max_iteration=3)
        expected_output = "- - 1\n  - 2\n  - 3\n  ...\n- 1: 2\n  3: 4\n  5: 6\n  7: 8"
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_max_item(self):
        data = [[1, 2, 3, 4, 5], {1:2, 3:4, 5:6, 7:8}]
        dumper = FlexibleDumper(max_item=3)
        expected_output = "- - 1\n  - 2\n  - 3\n  - 4\n  - 5\n- 1: 2\n  3: 4\n  5: 6\n  ..."
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_max_line(self):
        data = [1, 2, 3, 4, 5]
        dumper = FlexibleDumper(max_line=3)
        expected_output = "- 1\n- 2\n- 3\n..."
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_max_len(self):
        data = {"a": "abcdefghijklmnopqrstuvwxyz"}
        dumper = FlexibleDumper(max_len=10)
        expected_output = "a: abcdefg..."
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

    def test_all_constraints(self):
        data = [[1, 2, 3, 4, 5, 6], [2, "abcdefghijklmnopq"], {"a": 1, "b": 2, 5: [[], [1, 5, []]], 2: 3}, [1, [1, [[1, 2]]]], 6]
        dumper = FlexibleDumper(max_depth=2, max_iteration=5, max_item=3, max_line=14, max_len=20)
        expected_output = "- - 1\n  - 2\n  - 3\n  - 4\n  - 5\n  ...\n- - 2\n  - abcdefghijklmnop...\n- a: 1\n  b: 2\n  5: \n    - ...\n  ...\n- - 1\n..."
        result = dumper.dump(data)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
