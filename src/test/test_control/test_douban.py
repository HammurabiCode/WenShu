import os
# os.chdir('../../..')
import unittest


class TestDoubanQuota(unittest.TestCase):
    def test_get_quota(self):
        from src.control.douban.Quota import get_quota
        for book_id in [1012611]:
            get_quota(book_id)


if __name__ == '__main__':
    unittest.main()
