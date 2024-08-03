import requests

class ChatBotAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def add_command(self, command, response):
        url = f"{self.base_url}/add_command"
        payload = {
            "command": command,
            "response": response
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Команда добавлена успешно!"
        else:
            return f"Ошибка при добавлении команды: {response.json()}"

    def get_response(self, message):
        url = f"{self.base_url}/get_response"
        payload = {
            "message": message
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Ошибка при получении ответа."
