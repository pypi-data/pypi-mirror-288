import unittest
from src.parsec import chunks

class TestChunksFunction(unittest.TestCase):

    def test_chunks_normal(self):
        # 正常list的分割
        self.assertEqual(list(chunks([1, 2, 3, 4, 5], 2)), [[1, 2], [3, 4], [5]])

    def test_chunks_length_one(self):
        # 长度为1 的列表
        self.assertEqual(list(chunks([1], 1)), [[1]])

    def test_chunks_empty_list(self):
        # 长度为0的列表
        self.assertEqual(list(chunks([], 2)), [])

    def test_chunks_split_one(self):
        # 分割数为 1
        self.assertEqual(list(chunks([1, 2, 3], 1)), [[1], [2], [3]])

    def test_chunks_split_zero(self):
        # 分割数为 0，预期抛出ValueError异常
        with self.assertRaises(ValueError):
            list(chunks([1, 2, 3], 0))

    def test_chunks_negative_number(self):
        # 分割数为负数，预期抛出ValueError异常
        result = list(chunks([1, 2, 3], -2))
        self.assertListEqual(result, [])


if __name__ == '__main__':
    unittest.main()
