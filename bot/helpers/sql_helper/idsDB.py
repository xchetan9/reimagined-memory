import os

def search_parent(chat_id):
    try :
        with open(f"bot/data/id{chat_id}.txt","r") as f:
            parent_id = f.read()
        return parent_id
    except FileNotFoundError :
        return "root"

def _set(chat_id, parent_id):
    with open(f"bot/data/id{chat_id}.txt","w") as f:
        f.write(parent_id)

def _clear(chat_id):
    os.remove(f"bot/data/id{chat_id}.txt")