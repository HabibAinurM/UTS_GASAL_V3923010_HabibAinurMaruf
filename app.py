from flask import Flask, render_template, request

app = Flask(__name__)

# Tabel substitusi karakter untuk Caesar Cipher
encryption_table = {
    'A': 'H', 'B': 'A', 'C': 'B', 'D': 'I', 'E': 'C',
    'F': 'D', 'G': 'E', 'H': 'F', 'I': 'G', 'J': 'H',
    'K': 'J', 'L': 'K', 'M': 'L', 'N': 'M', 'O': 'N',
    'P': 'O', 'Q': 'P', 'R': 'Q', 'S': 'R', 'T': 'S',
    'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
    'Z': 'Z'
}

# Fungsi untuk mengenkripsi teks menggunakan Caesar Cipher
def encrypt_text(text, table):
    encrypted_text = ""
    text = text.upper()

    for char in text:
        if char in table:
            encrypted_text += table[char]
        else:
            encrypted_text += char

    return encrypted_text

# Fungsi untuk mendekripsi teks menggunakan Caesar Cipher
def decrypt_text(text, table):
    decrypted_text = ""

    for char in text:
        original_char = next((k for k, v in table.items() if v == char), None)
        if original_char is not None:
            decrypted_text += original_char
        else:
            decrypted_text += char

    return decrypted_text

# Fungsi untuk enkripsi Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')

            if char.islower():
                ciphertext += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            else:
                ciphertext += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))

            key_index += 1
        else:
            ciphertext += char
    return ciphertext

# Fungsi untuk dekripsi Vigenere Cipher
def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')

            if char.islower():
                plaintext += chr(((ord(char) - ord('a') - shift + 26) % 26) + ord('a'))
            else:
                plaintext += chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))

            key_index += 1
        else:
            plaintext += char
    return plaintext

@app.route("/", methods=["GET", "POST"])
def index():
    caesar_result = ""
    vigenere_result = ""
    if request.method == "POST":
        action = request.form["action"]
        
        if action in ["Enkripsi Caesar", "Dekripsi Caesar"]:
            text = request.form["text"]
            if action == "Enkripsi Caesar":
                caesar_result = encrypt_text(text, encryption_table)
            elif action == "Dekripsi Caesar":
                caesar_result = decrypt_text(text, encryption_table)

        elif action in ["Enkripsi Vigenere", "Dekripsi Vigenere"]:
            plaintext = request.form["plaintext"]
            key = request.form["key"]

            if action == "Enkripsi Vigenere":
                vigenere_result = vigenere_encrypt(plaintext, key)
            elif action == "Dekripsi Vigenere":
                vigenere_result = vigenere_decrypt(plaintext, key)

    return render_template("index.html", caesar_result=caesar_result, vigenere_result=vigenere_result)

if __name__ == "__main__":
    app.run(debug=True)
