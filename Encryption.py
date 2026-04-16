import hmac
import hashlib
import secrets

def make_master_key():
    return secrets.token_bytes(32)

def make_keys(master_key, nonce):
    key1 = hmac.new(master_key, b"vigenere"  + nonce, hashlib.sha256).digest()
    key2 = hmac.new(master_key, b"solitaire" + nonce, hashlib.sha256).digest()
    key3 = hmac.new(master_key, b"xor"       + nonce, hashlib.sha256).digest()
    return key1, key2, key3

def vigenere_encrypt(text, key):
    output = []
    for i, letter in enumerate(text):
        if letter.isalpha():
            shift = key[i % len(key)] % 26
            base  = ord('A') if letter.isupper() else ord('a')
            new_letter = chr((ord(letter) - base + shift) % 26 + base)
            output.append(new_letter)
        else:
            output.append(letter)
    return ''.join(output)

def vigenere_decrypt(text, key):
    output = []
    for i, letter in enumerate(text):
        if letter.isalpha():
            shift = key[i % len(key)] % 26
            base  = ord('A') if letter.isupper() else ord('a')
            new_letter = chr((ord(letter) - base - shift) % 26 + base)
            output.append(new_letter)
        else:
            output.append(letter)
    return ''.join(output)

def solitaire_stream(key, length):
    deck = list(range(54))

    for i in range(53, 0, -1):
        j = key[i % len(key)] % (i + 1)
        deck[i], deck[j] = deck[j], deck[i]

    stream = []
    needed = length + 50

    while len(stream) < needed:
        i = deck.index(52)
        deck.insert((i + 1) % len(deck), deck.pop(i))

        i = deck.index(53)
        deck.insert((i + 2) % len(deck), deck.pop(i))

        a, b = sorted([deck.index(52), deck.index(53)])
        deck = deck[b+1:] + deck[a:b+1] + deck[:a]

        last = deck[-1]
        if last < 53:
            deck = deck[last:] + deck[:last] + [deck[-1]]

        top = deck[0]
        if top < 53:
            stream.append(deck[top] % 256)

    return stream[50:50 + length]

def xor_mix(data, key3, sol_stream):
    output = []
    for i, byte in enumerate(data):
        hmac_byte  = hmac.new(key3, i.to_bytes(4, 'big'), hashlib.sha256).digest()[0]
        mixed_byte = byte ^ hmac_byte ^ sol_stream[i]
        output.append(mixed_byte)
    return bytes(output)

def rail_fence_encrypt(text, rails=3):
    rows = [[] for _ in range(rails)]
    r, going_down = 0, True

    for ch in text:
        rows[r].append(ch)
        if r == rails - 1: going_down = False
        elif r == 0:       going_down = True
        r += 1 if going_down else -1

    return ''.join(''.join(row) for row in rows)

def rail_fence_decrypt(text, rails=3):
    n = len(text)
    pattern, r, going_down = [], 0, True

    for _ in range(n):
        pattern.append(r)
        if r == rails - 1: going_down = False
        elif r == 0:       going_down = True
        r += 1 if going_down else -1

    order  = sorted(range(n), key=lambda i: pattern[i])
    result = [''] * n
    for pos, ch in zip(order, text):
        result[pos] = ch
    return ''.join(result)

def encrypt(message, master_key):
    nonce = secrets.token_bytes(16)
    key1, key2, key3 = make_keys(master_key, nonce)

    step1 = vigenere_encrypt(message, key1)
    step2 = step1.encode()
    step3 = solitaire_stream(key2, len(step2))
    step4 = xor_mix(step2, key3, step3)
    step5 = rail_fence_encrypt(step4.hex(), rails=3)

    return nonce.hex() + ":" + step5

def decrypt(package, master_key):
    nonce_hex, ciphertext = package.split(":")
    nonce = bytes.fromhex(nonce_hex)
    key1, key2, key3 = make_keys(master_key, nonce)

    step5 = rail_fence_decrypt(ciphertext, rails=3)
    step4 = bytes.fromhex(step5)
    step3 = solitaire_stream(key2, len(step4))
    step2 = xor_mix(step4, key3, step3)
    step1 = step2.decode()
    message = vigenere_decrypt(step1, key1)

    return message

master_key = make_master_key()
message    = "Hello! This is my secret message."

print("Original :", message)

encrypted  = encrypt(message, master_key)
print("Encrypted:", encrypted)

decrypted  = decrypt(encrypted, master_key)
print("Decrypted:", decrypted)

if decrypted == message:
    print("\n✅ Works perfectly!")
else:
    print("\n❌ Something went wrong.")