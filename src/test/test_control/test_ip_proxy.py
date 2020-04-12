import unittest


class TestIPProxy(unittest.TestCase):
    def test_get_proxy(self):
        from src.control.ip_proxy.proxy_xici import get_proxy
        res = get_proxy()
        print(res)


if __name__ == "__main__":
    unittest.main()
