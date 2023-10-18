from random import randint
dictionary = {'с': 30846, 'т': 38288, 'а': 47086, 'р': 22374, 'и': 36418, 'к': 21475, 'ы': 11036, 'б': 10721, 'ч': 9433, 'л': 27765, 'о': 68455, 'д': 17799, 'н': 38806, 'в': 24317, 'е': 50576, 'й': 5470, 'г': 10004, 'ь': 12963, 'ф': 900, 'м': 19223, 'у': 17107, 'ж': 6505, 'я': 12442, 'х': 4969, 'п': 15871, 'з': 10255, 'ш': 4613, 'ю': 2926, 'щ': 1963, 'ц': 1362, 'э': 2002, 'ъ': 120}
def main():
    unfiltered = "unfiltered.txt"
    filtered = "filtered.txt"
    encoded = {"r2.txt": 2, "r3.txt": 3, "r4.txt": 4, "r5.txt": 5, "r10.txt": 10, "r15.txt": 15, "r20.txt": 20}
    text_filter(unfiltered, filtered)
    for file in encoded.keys():
        encode(encoded[file], filtered, file)
        print(f"{file} ---> {reliability_index(file)}")
    print(f"{file} ---> {reliability_index(filtered)}")
    length_and_text = find_key_length(17, "wtf.txt")
    key = decode_of_key(length_and_text[0], length_and_text[1])
    print(key)
    decode_text("возвращениеджинна", "wtf.txt")
    with open("wtf_decrypted.txt", 'r', encoding="utf-8") as file:
        text = file.read()

def text_filter(unfiltered_file, filtered_file):
    with open(unfiltered_file, 'r', encoding="utf8") as file:
        text = file.read().lower()
    new_string = ""
    allowed = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    for symbol in text:
        if symbol in allowed:
            new_string += symbol
        elif symbol == 'ё':
            new_string += 'е'
    final_text = ' '.join(new_string.split())
    with open(filtered_file, 'w', encoding="utf-8") as file:
        file.write(final_text)

def encode(r, filtered_file, output_file):
    with open(filtered_file, 'r', encoding="utf8") as file:
        text = file.read()
    num = randint(0, len(text))
    key = text[0:r]
    encoded_text = ""
    i = 0
    for symbol in text:
        encoded_text += chr((ord(symbol) + ord(key[i % r])) % 32 + 1072)
        i += 1
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(encoded_text)
def letter_count(text:str):
    dictionary = {"total" : 0}
    for symbol in text:
        dictionary["total"] += 1
        if symbol not in dictionary:
            dictionary[symbol] = 1
        else:
            dictionary[symbol] += 1
    return dictionary
def reliability_index(filtered_file):
    with open(filtered_file, 'r', encoding="utf-8") as file:
        text = file.read()
    length = len(text)
    index = 0
    dictionary = letter_count(text)
    for key in dictionary.keys():
        if key != "total":
            index += dictionary[key]*(dictionary[key]-1)
    result = index/(length*(length-1))
    return result

def reliability_index_text(text):
    length = len(text)
    index = 0
    dictionary = letter_count(text)
    for key in dictionary.keys():
        if key != "total":
            index += dictionary[key]*(dictionary[key]-1)
    result = index/(length*(length-1))
    return result
def find_key_length(r, encoded_file):
    with open(encoded_file, 'r', encoding="utf-8") as file:
        text = file.read()
    splited_text = [""]*r
    ideal_i = 0.05644457241434476 #взяв значення з першої лаби
    for index in range(len(text)):
        splited_text[index % r] += text[index]
    check_sum = 0
    for part_text in splited_text:
        check_sum += reliability_index_text(part_text)
    check_sum = check_sum/r
    return [splited_text, check_sum]

def most_common_char(input_string):
    most_common = max(input_string, key=input_string.count)
    return most_common

def decode_of_key(text, key_length):
    key = ""
    i = 0
    for part_text in text:
        if i < 13:
            y = most_common_char(part_text)
            x = 'о'
            key += chr(((ord(y) - ord(x)) % 32) + 1072)
        else:
            y = most_common_char(part_text)
            x = 'о'
            key += chr(((ord(y) - ord(x)) % 32) + 1072)
        i+=1
    return key

def decode_text(key, encoded_file):
    with open(encoded_file, 'r', encoding="utf-8") as file:
        encrypted_text = file.read()
    decrypted_text = ""
    key_length = len(key)
    for i in range(len(encrypted_text)):
        encrypted_char = encrypted_text[i]
        key_char = key[i % key_length]
        decrypted_char = chr((ord(encrypted_char) - ord(key_char)) % 32 + 1072)
        decrypted_text += decrypted_char
    with open("wtf_decrypted.txt", 'w', encoding="utf-8") as file:
        file.write(decrypted_text)

if __name__ == "__main__":
    main()

