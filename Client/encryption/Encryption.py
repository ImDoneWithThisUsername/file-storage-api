from . import RSA
from PIL import Image

# encrypt image
def encrypt_image(in_path:str, out_path:str, key:int):

    # # open file for reading purpose
    # fin = open(in_path, 'rb')
    
    # # storing image data in variable "image"
    # image = fin.read()
    # fin.close()
    
    # # converting image into byte array to perform decryption easily on numeric data
    # image = bytearray(image)

    # # performing XOR operation on each value of bytearray
    # for index, values in enumerate(image):
    #     image[index] = values ^ key
    # # opening file for writing purpose
    # fin = open(out_path, 'wb')
    
    # # writing decryption data in image
    # fin.write(image)
    # fin.close()
    picture = Image.open(in_path)
    # Get the size of the image

    width, height = picture.size
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            current_color = picture.getpixel( (x,y) )
            ####################################################################
            # Do your logic here and create a new (R,G,B) tuple called new_color
            ####################################################################
            new_color = (current_color[0]^key,current_color[1]^key,current_color[2]^key)
            picture.putpixel( (x,y), new_color)
    picture.save(out_path)


def hash_string( s:str,n:int = 32768) -> int:
    res = 0
    for c in s:
        c = ord(c)
        if c >= 100:
            res = (res*1000 + c) % n
        elif c >= 10:
            res = (res*100 + c) % n
        else:
            res = (res*10 + c) % n
    return res

def validate_sig(sig:int, data:str, pub_key:int, n:int):
    hashed = hash_string(data)
    dec_sig = RSA.power_mod(sig, pub_key, n)
    return hashed == dec_sig
