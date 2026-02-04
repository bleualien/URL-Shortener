import string


def generate_short_key(instance_id):
    id_num = instance_id + 100000
    characters = string.digits + string.ascii_letters
    base = len(characters)
    res = []

    # Simple Base62 conversion
    # id_num = instance_id
    while id_num > 0:
        res.append(characters[id_num % base])
        id_num //= base

    return "".join(reversed(res)) if res else "0"
