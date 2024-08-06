import requests

def send_sms(msg: str, user: str, password: str):
    try:
            encoded_msg = msg.replace(" ", "%20")
            
            url = f"https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={password}&msg={encoded_msg}"           
            
            response = requests.post(url)
            
            if response.status_code == 200:
                print("Message envoyé !")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Erreur : {e}")
