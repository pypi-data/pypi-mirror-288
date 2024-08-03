import unittest
from xasdesbotapi import ChatBotAPI

class TestChatBotAPI(unittest.TestCase):
    def setUp(self):
        self.api = ChatBotAPI("http://127.0.0.1:5000")

    def test_add_command(self):
        result = self.api.add_command("тест", "тестовый ответ")
        self.assertEqual(result, "Команда добавлена успешно!")

    def test_get_response(self):
        self.api.add_command("привет", "Привет!")
        response = self.api.get_response("привет")
        self.assertEqual(response, "Привет!")

if __name__ == '__main__':
    unittest.main()
