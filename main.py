import requests
import os
import keyboards

import time

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{self.token}/'
        self.last_update_id = None
        self.like = 0
        self.dislike = 0
        self.inline_like = 0
        self.inline_dislike = 0

    def get_updates(self):
        """
        Fetches updates from the Telegram API.
        :return: JSON response containing updates.
        """
        url = self.api_url + 'getUpdates'
        params = {'timeout': 100, 'offset': self.last_update_id}
        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, chat_id, text):
        """
        Sends a message to the specified chat.
        :param chat_id: ID of the chat where the message will be sent.
        :param text: Text of the message to send.
        """
        url = self.api_url + 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        requests.get(url, params=params)
    
    def send_photo(self, chat_id: int, photo: str):
        """
        Send photo

        Args:
            chat_id (int): chat id
            photo (str): photo
        """
        url = self.api_url + 'sendPhoto'
        json={'chat_id': chat_id, 
              'photo': photo, 
              'caption': f"Like count: {self.inline_like}\nDislike count: {self.dislike}", 
              'reply_markup': keyboards.inline_keyboard
            }
        requests.post(url, json=json)
        

    def handle_updates(self, updates):
        """
        Handles the incoming updates by processing each message and sending a response.
        :param updates: JSON response containing updates.
        """
        
        if 'result' in updates:
            for update in updates['result']:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    if update['message'].get('text')!=None:
                        text = update['message']['text']
                        # Respond to the received message
                        if text=='👍':
                            self.like += 1
                        if text == '👎':
                            self.dislike += 1
                        if text=='🆑':
                            self.like = 0
                            self.dislike = 0
                        self.send_message(chat_id, text=f"Like count: {self.like}\nDislike count: {self.dislike}")
                        # Update last_update_id to prevent reprocessing the same messages
                        self.last_update_id = update['update_id'] + 1
                    elif update['message'].get('photo')!=None:
                        photo = update['message']['photo'][0]['file_id']
                        self.send_photo(chat_id, photo)
                        
                        self.last_update_id = update['update_id'] + 1

    def run(self):
        """
        Runs the bot, continuously fetching updates and handling them.
        """
        while True:
            updates = self.get_updates()
            self.handle_updates(updates)
            time.sleep(0.3)

if __name__ == '__main__':
    # Replace with your bot's token
    TOKEN = os.environ['TOKEN'] 

    
    bot = TelegramBot(TOKEN)
    bot.run()
