from Crypto.Cipher import AES
import base64

from cocktails.localsettings import SHARE_KEY


def encrypt(clear_text):
    enc_secret = AES.new(SHARE_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return cipher_text


def decrypt(cipher_text):
    dec_secret = AES.new(SHARE_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val
