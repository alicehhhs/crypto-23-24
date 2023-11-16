import random
import hashlib
import string

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def ext_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = ext_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def mod_inverse(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1:
        return None  # Оберненого елемента не існує
    else:
        return (x % m + m) % m


def trial_division(n):
    if n < 2:
        return False
    for i in range(2, 100):
        if n % i == 0:
            return False
    return True


def is_prime_miller_rabin(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True

    def find_s_d(n):
        s = 0
        while n % 2 == 0:
            s += 1
            n //= 2
        return s, n

    s, d = find_s_d(n - 1)

    for i in range(k):
        a = random.randint(1, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        else:
            for j in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
                if x == 1:
                    return False
            if x == n - 1:
                continue
            return False

    return True


def generate_random_prime_number(min_value, max_value):
    while True:
        n = random.randint(min_value, max_value)
        if trial_division(n):
            if is_prime_miller_rabin(n):
                return n
        else:
            print(f"Кандидат що не пройшов: {n}")


def decimal_to_binary(decimal_number):
    binary_representation = bin(decimal_number)[2:]
    return binary_representation


def ConvertToInt_en(text, hash=False):
    num = 0
    if not hash:
        for char in text:
            num = num * 50000 + ord(char)
    else:
        for char in text:
            num = num * 256 + ord(char)
    return num

def ConvertToText_en(number):
    text = ""
    while number > 0:
        char_code = number % len(alphabet)
        text = alphabet[char_code] + text
        number //= len(alphabet)
    return text

def ConvertToInt_dec(text):
    num = 0
    for char in text:
        if char in alphabet:
            num = num * len(alphabet) + alphabet.index(char)
    return num


def ConvertToText_dec(num, hash=False):
    text = ""
    if not hash:
        while num > 0:
            char_code = num % 50000
            text = chr(char_code) + text
            num //= 50000
    else:
        while num > 0:
            char_code = num % 256
            text = chr(char_code) + text
            num //= 256
    return text


def GenerateKeyPair(p, q):
    n = p*q
    totient = (p-1)*(q-1)
    e = random.randint(2, totient - 1)
    (g, x, y) = ext_gcd(e, totient)
    while g > 1:
        e = random.randint(2, totient-1)
        (g, x, y) = ext_gcd(e, totient)
    d = mod_inverse(e, totient)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def split_blocks(text, max_block_size):
    blocks = []

    for i in range(0, len(text), 32):
        block = text[i:i + 32]
        blocks.append(block)

    for i in range(len(blocks)):
        while len(decimal_to_binary(ConvertToInt_en(blocks[i]))) > max_block_size:
            half_size = len(blocks[i]) // 2
            block1 = blocks[i][:half_size]
            block2 = blocks[i][half_size:]
            blocks[i] = block1
            blocks.insert(i + 1, block2)

    return blocks


def Encrypt(input_text, key, hash=False):
    e, n = key
    if hash:
        text_in_num = ConvertToInt_en(input_text, hash)
        number_encrypted = pow(text_in_num, e, n)
        text_encrypted = ConvertToText_en(number_encrypted)
        return text_encrypted

    mes_len_in_num = len(decimal_to_binary(ConvertToInt_en(input_text)))

    if mes_len_in_num >= len(decimal_to_binary(n)):
        blocks = split_blocks(input_text, len(decimal_to_binary(n)) - 1)
        enc_text = []
        for block in blocks:
            text_in_num = ConvertToInt_en(block)
            number_encrypted = pow(text_in_num, e, n)
            text_encrypted = ConvertToText_en(number_encrypted)
            enc_text.append(text_encrypted)
        return enc_text
    text_in_num = ConvertToInt_en(input_text)
    number_encrypted = pow(text_in_num, e, n)
    text_encrypted = ConvertToText_en(number_encrypted)
    return text_encrypted


def Decrypt(encrypted_text, key, hash=False):
    d, n = key
    if isinstance(encrypted_text, list):
        dec_text = ""
        for block in encrypted_text:
            number_encrypted = ConvertToInt_dec(block)
            number_decrypted = pow(number_encrypted, d, n)
            text_decrypted = ConvertToText_dec(number_decrypted, hash)
            dec_text += text_decrypted
        return dec_text
    number_encrypted = ConvertToInt_dec(encrypted_text)
    number_decrypted = pow(number_encrypted, d, n)
    text_decrypted = ConvertToText_dec(number_decrypted, hash)
    return text_decrypted


def Sign(input_text, my_private_key, public_key):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_text.encode('utf-8'))
    sha256_hash_value = sha256_hash.hexdigest()
    print(sha256_hash_value)
    hash_encrypted_with_prv = Encrypt(sha256_hash_value, my_private_key, True)
    print(f"Signature: {hash_encrypted_with_prv}")

    hash_encrypted_with_pbl = Encrypt(hash_encrypted_with_prv, public_key)
    print(f"Signature encrypted with public key: {hash_encrypted_with_pbl}")
    return hash_encrypted_with_pbl


def Verify(input_text, sign, public_key, my_private_key):
    hash_decrypted_with_prv = Decrypt(sign, my_private_key)
    print(f"Signature decrypted with private key: {hash_decrypted_with_prv}")
    hash_decrypted_with_pbl = Decrypt(hash_decrypted_with_prv, public_key, True)
    print(f"Hash decrypted with public key(signature is verified): {hash_decrypted_with_pbl}")

    sha256_hash_cal = hashlib.sha256()
    sha256_hash_cal.update(input_text.encode('utf-8'))
    sha256_hash_value = sha256_hash_cal.hexdigest()
    print("Hash calculated from received message: ", sha256_hash_value)

    if hash_decrypted_with_pbl == sha256_hash_value:
        return True
    else:
        return False


def create_message_for_abonent(public_key, length, my_private_key):
    characters = (string.ascii_letters + string.digits + ' ' + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + 'ґєіїҐЄІЇ' + '你好' + '中文' + ' ')
    random_message = ''.join(random.choice(characters) for i in range(length))
    print("Generated message: ", random_message)
    encrypted_message = Encrypt(random_message, public_key)
    signed_message = Sign(random_message, my_private_key, public_key)
    message = (encrypted_message, signed_message)
    return message


def receive_message_from_abonent(message, my_private_key, public_key):
    enc_mes, signed_mes = message
    decrypted_message = Decrypt(enc_mes, my_private_key)
    print("Decrypted message: ", decrypted_message)
    ver_mes = Verify(decrypted_message, signed_mes, public_key, my_private_key)
    if ver_mes:
        print("Whereas decrypted and calculated hashes match, then message isn`t tampered\n")
    else:
        print("Message is tampered by someone\n")


print("Task1-2")
print("-----------------------------------------------------------------------")
p1 = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)
q1 = generate_random_prime_number(100000000000000000000000000000000000000000000000000000000000000000000000000000, 555555555555555555555555555555555555555555555555555555555555555555555555555555)

p2 = generate_random_prime_number(555555555555555555555555555555555555555555555555555555555555555555555555555555, 999999999999999999999999999999999999999999999999999999999999999999999999999999)
q2 = generate_random_prime_number(555555555555555555555555555555555555555555555555555555555555555555555555555555, 999999999999999999999999999999999999999999999999999999999999999999999999999999)

print(f"\nПерша пара простих чисел: p = {p1}\nq = {q1}")
print(f"Довжина p = {len(decimal_to_binary(p1))} bit, q = {len(decimal_to_binary(q1))} bit\n")
print(f"Дурга пара простих чисел: p1= {p2}\nq1 = {q2}")
print(f"Довжина p1 = {len(decimal_to_binary(p2))} bit, q1 = {len(decimal_to_binary(q2))} bit")
print("-----------------------------------------------------------------------\n")


print("Task3")
print("-----------------------------------------------------------------------")
key1 = GenerateKeyPair(p1, q1)
key2 = GenerateKeyPair(p2, q2)

e1, d1 = key1
e2, d2 = key2

print(f"Публічний ключ: {e1}\nПриватний ключ: {d1}\n")
print(f"Публічний ключ1: {e2}\nПриватний ключ1: {d2}")
print("-----------------------------------------------------------------------\n")


print("Task4-5")
print("-----------------------------------------------------------------------")
print("From A to B")
message_from_A = create_message_for_abonent(e2, 300, d1)
print(f"Encrypted message and encrypted signature from A to B: {message_from_A}\n")
receive_message_from_abonent(message_from_A, d2, e1)

print("From B to A")
message_from_B = create_message_for_abonent(e1, 300, d2)
print(f"Encrypted message and encrypted signature from B to A: {message_from_B}\n")
receive_message_from_abonent(message_from_B, d1, e2)
print("-----------------------------------------------------------------------\n")

