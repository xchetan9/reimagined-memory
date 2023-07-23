import os

def search_name(chat_id):
    try :
        with open(f"bot/data/name{chat_id}.txt","r") as f:
            parent_id = f.read()
        return parent_id
    except FileNotFoundError :
        return ""
    
def search_sameparent(chat_id):
    try :
        with open(f"bot/data/self{chat_id}.txt","r") as f:
            parent_id = f.read()
        return parent_id
    except FileNotFoundError :
        return None



def _set(chat_id, parent_id):
    with open(f"bot/data/name{chat_id}.txt","w") as f:
        f.write(parent_id)


def _setsame(chat_id, parent_id):
    with open(f"bot/data/self{chat_id}.txt","w") as f:
        f.write(parent_id)

def _clear(chat_id):
    os.remove(f"bot/data/name{chat_id}.txt")

def removesame(chat_id):
    os.remove(f"bot/data/self{chat_id}.txt")