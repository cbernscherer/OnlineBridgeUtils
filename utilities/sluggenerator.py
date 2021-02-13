from secrets import choice

base_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
base = [c for c in base_set]

def create_random_slug(length=16):
    def work():
        slug = ""
        for i in range(0, length):
            slug += choice(base)

        return slug

    return work