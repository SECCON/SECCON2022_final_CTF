import os
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.number import getPrime


p = getPrime(128)

xs = [random.randint(1, 2**64) for _ in range(4)]

a = random.randint(1, p)
b = random.randint(1, p)
c = random.randint(1, p)
d = random.randint(1, p)
e = random.randint(1, p)  # unknown

xs.append((a*xs[-4] + b*xs[-3] + c*xs[-2] + d*xs[-1] + e) % p)
xs.append((a*xs[-4] + b*xs[-3] + c*xs[-2] + d*xs[-1] + e) % p)
xs.append((a*xs[-4] + b*xs[-3] + c*xs[-2] + d*xs[-1] + e) % p)

outs = xs[-3:]


# encryption
FLAG = os.getenv("FLAG", "fake{the_flag_is_a_lie}")
key = 0
for x in xs[:4]:
    key <<= 64
    key += x
key = int(key).to_bytes(32, "little")
iv = get_random_bytes(16)  # public
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG.encode(), 16))  # public

# output
print(f"p = {p}")
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"d = {d}")
print(f"outs = {outs}")
print(f"iv = 0x{iv.hex()}")
print(f"ct = 0x{ct.hex()}")