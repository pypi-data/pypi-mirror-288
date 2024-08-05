import random
import string


class Random:
    class String:
        def make(length: int = 8):
            character_set = (
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            )
            return "".join(random.choices(character_set, k=length))
