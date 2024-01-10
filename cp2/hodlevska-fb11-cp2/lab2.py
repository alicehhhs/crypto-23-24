import re
from collections import Counter
from statistics import mean


def clearing_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        original = infile.read()

    edited = re.sub(r'[^а-яА-Я]', '', original)
    edited = edited.replace("ё", "е").lower()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(edited)


alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж',
            'з', 'и', 'й', 'к', 'л', 'м', 'н',
            'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
            'ь', 'э', 'ю', 'я']

m = len(alphabet)
key_2 = 'ум'
key_3 = 'боа'
key_4 = 'пить'
key_5 = 'гумус'
key_15 = 'самоуничтожение'


def vigenere(input_text, key):
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()

    ciphred = []
    key_length = len(key)
    encrypted_text = ''

    for i in range(len(text)):
        key_i = alphabet.index(key[i % key_length])
        text_i = alphabet.index(text[i])
        ciphred.append((text_i + key_i) % m)
    for j in ciphred:
        encrypted_text += alphabet[j]
    return encrypted_text


encrypted_data = {
    "encrypted_2.txt": vigenere('clear_toast.txt', key_2),
    "encrypted_3.txt": vigenere('clear_toast.txt', key_3),
    "encrypted_4.txt": vigenere('clear_toast.txt', key_4),
    "encrypted_5.txt": vigenere('clear_toast.txt', key_5),
    "encrypted_15.txt": vigenere('clear_toast.txt', key_15)
}
'''
for file, data in encrypted_data.items():
    with open(file, 'w', encoding='utf-8') as outfile:
        outfile.write(data)
'''


def index_vid(text):
    n = len(text)
    freq = Counter(text)
    big_n = 0

    for num in freq.values():
        big_n += num * (num - 1)

    ind = big_n / (n * (n - 1))
    return ind


'''
for file in encrypted_data.keys():
    with open(file, 'r', encoding='utf-8') as file_:
        text = file_.read()
    print(f"for {file}: {index_vid(text)}")
with open('clear_toast.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    print(f"for open text: {index_vid(text)}")
'''


def key_period(input_text, key_len):
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()
    key_length_list = []
    for i in range(key_len):
        r = index_vid(text[i::key_len])
        key_length_list.append(r)
    return mean(key_length_list)


def frequency(text):
    all_letters = len(text)
    frequency_dict = {}

    for letter in alphabet:
        count = text.count(letter)
        freq = round(count / all_letters, 4)
        frequency_dict[letter] = freq
    most_common = max(frequency_dict, key=frequency_dict.get)
    return most_common


most_common_rus = alphabet.index('о')


def guess_key(input_text):
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()
    r = 17
    ks = []
    for i in range(r):
        enc_freq = alphabet.index(frequency(text[i::r]))
        k = (enc_freq - most_common_rus) % m
        ks.append(alphabet[k])
    kes = ''.join(ks)
    print(kes)


def decrypt(input_text, key, output_file):
    with open(input_text, 'r', encoding='utf-8') as file:
        text = file.read()
    decrypted = []
    decrypted_text = ''
    for i in range(len(text)):
        key_i = alphabet.index(key[i % len(key)])
        text_i = alphabet.index(text[i])
        decrypted.append((text_i - key_i) % m)
    for j in decrypted:
        decrypted_text += alphabet[j]
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)


guess_key('11var.txt')
decrypt('11var.txt', 'венецианскийкупец', '11var_decrypted.txt')
