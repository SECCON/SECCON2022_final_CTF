import secrets
import time
import sys
import os

flag = os.environ.get("FLAG", "neko{neko neko kawaii}")
key = secrets.randbits(64)


def crc64(data: bytes, init: int) -> int:
    g = 0xcd8da4ff37e45ec3
    crc = init

    for x in data:
        crc = crc ^ x
        for _ in range(8):
            crc = ((crc >> 1) ^ (g * (crc & 1))) & 0xffffffffffffffff
    return crc


def auth(code: int, t: int) -> bool:
    return crc64((key ^ t).to_bytes(8, "little"), code) == code


while True:
    print("[A]uthenticate yourself")
    print("[H]int for pre-shared key")
    choice = input("> ").strip()
    if choice == "A":
        code = int(input("code: "), 16)
        assert 0 <= code < 2**64

        # key is changed in every 5 seconds
        t = int(time.time()) // 5 * 5
        if auth(code, t):
            print(flag)
            sys.exit(0)
        print("WRONG code")

    elif choice == "H":
        t = int(time.time()) // 5 * 5
        hint = crc64(b"hint", crc64((key ^ t).to_bytes(8, "little"), 0))
        print(f"hint: {hint:x}")

    else:
        sys.exit(0)
