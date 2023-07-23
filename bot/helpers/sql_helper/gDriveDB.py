import pickle
import os

def _set(chat_id, credential_string):
    with open(f"bot/data/gd{chat_id}.bat",'wb') as f :
        f.write(pickle.dumps(credential_string))

def search(chat_id):
    try :
        with open(f"bot/data/gd{chat_id}.bat",'rb') as f :
            return pickle.loads(f.read())
    except FileNotFoundError :
        return None

def _clear(chat_id):
    os.remove(f"bot/data/gd{chat_id}.bat")
