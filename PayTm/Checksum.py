# pip install pycryptodome
import base64
import string
import random
import hashlib
# import crypto
# import sys
# sys.modules['Crypto']
# from Crypto.Cipher 
# import AES
from Crypto.Cipher  import AES



IV = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16


def generate_checksum(param_dict, merchant_key, salt=None):
    params_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)

def generate_refund_checksum(param_dict, merchant_key, salt=None):
    for i in param_dict:
        if("|" in param_dict[i]):
            param_dict = {}
            exit()
    params_string = __get_param_string__(param_dict)
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def generate_checksum_by_str(param_str, merchant_key, salt=None):
    params_string = param_str
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def verify_checksum(param_dict, merchant_key, checksum):
    # Remove checksum
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')

    # Get salt
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum(param_dict, merchant_key, salt=salt)
    return calculated_checksum == checksum

def verify_checksum_by_str(param_str, merchant_key, checksum):
    # Remove checksum
    #if 'CHECKSUMHASH' in param_dict:
        #param_dict.pop('CHECKSUMHASH')

    # Get salt
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(param_str, merchant_key, salt=salt)
    return calculated_checksum == checksum



def __id_generator__(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def __get_param_string__(params):
    params_string = []
    for key in sorted(params.keys()):
        if("REFUND" in params[key] or "|" in params[key]):
            respons_dict = {}
            exit()
        value = params[key]
        params_string.append('' if value == 'null' else str(value))
    return '|'.join(params_string)


__pad__ = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
__unpad__ = lambda s: s[0:-ord(s[-1])]


def __encode__(to_encode, iv, key):
    # Pad
    to_encode = __pad__(to_encode)
    # Encrypt
    c = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    to_encode = c.encrypt(to_encode.encode('utf-8'))
    # Encode
    to_encode = base64.b64encode(to_encode)
    return to_encode.decode("UTF-8")


def __decode__(to_decode, iv, key):
    # Decode
    to_decode = base64.b64decode(to_decode)
    # Decrypt
    c = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    to_decode = c.decrypt(to_decode)
    if type(to_decode) == bytes:
        # convert bytes array to str.
        to_decode = to_decode.decode()
    # remove pad
    return __unpad__(to_decode)


if __name__ == "__main__":
    params = {
        "MID": "mid",
        "ORDER_ID": "order_id",
        "CUST_ID": "cust_id",
        "TXN_AMOUNT": "1",
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "xxxxxxxxxxx"
    }

    print(verify_checksum(
        params, 'xxxxxxxxxxxxxxxx',
        "CD5ndX8VVjlzjWbbYoAtKQIlvtXPypQYOg0Fi2AUYKXZA5XSHiRF0FDj7vQu66S8MHx9NaDZ/uYm3WBOWHf+sDQAmTyxqUipA7i1nILlxrk="))

    # print(generate_checksum(params, "xxxxxxxxxxxxxxxx"))


# import base64
# import string
# import random
# import hashlib
# import sys

# from Crypto.Cipher import AES


# iv = '@@@@&&&&####$$$$'
# BLOCK_SIZE = 16

# if (sys.version_info > (3, 0)):
#     __pad__ = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
# else:
#     __pad__ = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# __unpad__ = lambda s: s[0:-ord(s[-1])]    

# def encrypt(input, key):
#     input = __pad__(input)
#     c = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
#     input = c.encrypt(input)
#     input = base64.b64encode(input)
#     return input.decode("UTF-8")

# def decrypt(encrypted, key):
#     encrypted = base64.b64decode(encrypted)
#     c = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
#     param = c.decrypt(encrypted)
#     if type(param) == bytes:
#         param = param.decode()
#     return __unpad__(param)

# def generateSignature(params, key):
#     if not type(params) is dict and not type(params) is str:
#         raise Exception("string or dict expected, " + str(type(params)) + " given")
#     if type(params) is dict:
#         params = getStringByParams(params)
#     return generateSignatureByString(params, key)

# def verifySignature(params, key, checksum):
#     if not type(params) is dict and not type(params) is str:
#         raise Exception("string or dict expected, " + str(type(params)) + " given")
#     if "CHECKSUMHASH" in params:
#         del params["CHECKSUMHASH"]
        
#     if type(params) is dict:
#         params = getStringByParams(params)
#     return verifySignatureByString(params, key, checksum)

# def generateSignatureByString(params, key):    
#     salt = generateRandomString(4)
#     return calculateChecksum(params, key, salt)

# def verifySignatureByString(params, key, checksum):
#     paytm_hash = decrypt(checksum, key)    
#     salt = paytm_hash[-4:]
#     return paytm_hash == calculateHash(params, salt)

# def generateRandomString(length):
#     chars = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))
#     return chars

# def getStringByParams(params):
#     params_string = []
#     for key in sorted(params.keys()):
#         value = params[key] if params[key] is not None and params[key].lower() != "null" else ""
#         params_string.append(str(value))
#     return '|'.join(params_string)

# def calculateHash(params, salt):    
#     finalString = '%s|%s' % (params, salt)
#     hasher = hashlib.sha256(finalString.encode())
#     hashString = hasher.hexdigest() + salt
#     return hashString

# def calculateChecksum(params, key, salt): 
#     hashString = calculateHash(params, salt)
#     return encrypt(hashString, key)