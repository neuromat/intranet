import string
import random


def generate_secret_key(archive):

    f = open(archive, "w")

    # Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
    chars = ''.join([string.ascii_letters,
                     string.digits,
                     string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

    SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

    f.write('SECRET_KEY = ' + '"' + SECRET_KEY + '"')
    f.close()
