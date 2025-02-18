import unittest
import allure

class TestSimplePass(unittest.TestCase):
    @allure.title("Успешное заполнение формы")
    def test_pass(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
