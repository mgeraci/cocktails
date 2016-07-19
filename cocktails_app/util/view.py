OK_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?:"

def is_safe(str):
    return [x for x in str if x.lower() not in OK_CHARS] == []
