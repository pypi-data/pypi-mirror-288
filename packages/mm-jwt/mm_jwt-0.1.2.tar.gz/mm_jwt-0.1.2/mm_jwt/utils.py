from django.conf import settings
import pytz


pytz_UTC = pytz.utc


def __XOR(raw:str) -> str:
    test = ''
    for i in raw:
        ascii_code = ord(i)
        if ascii_code == 8962:
            ascii_code = 127
        xored = ascii_code ^ 23
        test += chr(xored)
    
    return test


def cipher(raw:str) -> str:
    alg_list = {'XOR': __XOR, } # TODO complete
    
    algorithm = settings.CUSTOM_TOKEN_CONF.get('algorithm')
    if algorithm is None:
        raise Exception('no algorithm specified')
    
    if algorithm not in alg_list.keys():
        raise Exception('desired algorithm not accessible')

    cipher_text = alg_list[algorithm](raw=raw)

    return cipher_text

