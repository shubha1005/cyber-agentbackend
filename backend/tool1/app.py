# from flask import Flask, request, jsonify, Blueprint
# from flask_cors import CORS
# from Crypto.Cipher import AES, DES, PKCS1_OAEP
# from Crypto.PublicKey import RSA
# from Crypto.Util.Padding import pad, unpad
# from base64 import b64encode, b64decode

# # Define the Blueprint for tool1
# tool1 = Blueprint('tool1', __name__)

# # Enable CORS for the blueprint
# CORS(tool1)

# # AES Encryption/Decryption
# def aes_encrypt(data, key):
#     cipher = AES.new(key, AES.MODE_CBC)
#     ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
#     return b64encode(cipher.iv + ciphertext).decode()

# def aes_decrypt(data, key):
#     raw = b64decode(data)
#     iv, ciphertext = raw[:16], raw[16:]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

# # DES Encryption/Decryption
# def des_encrypt(data, key):
#     cipher = DES.new(key, DES.MODE_CBC)
#     ciphertext = cipher.encrypt(pad(data.encode(), DES.block_size))
#     return b64encode(cipher.iv + ciphertext).decode()

# def des_decrypt(data, key):
#     raw = b64decode(data)
#     iv, ciphertext = raw[:8], raw[8:]
#     cipher = DES.new(key, DES.MODE_CBC, iv)
#     return unpad(cipher.decrypt(ciphertext), DES.block_size).decode()

# # RSA Encryption/Decryption
# # def generate_rsa_keys():
# #     key = RSA.generate(2048)
# #     private_key = key.export_key()
# #     public_key = key.publickey().export_key()
# #     return private_key, public_key

# # def rsa_encrypt(data, public_key):
# #     rsa_key = RSA.import_key(public_key)
# #     cipher = PKCS1_OAEP.new(rsa_key)
# #     return b64encode(cipher.encrypt(data.encode())).decode()

# # def rsa_decrypt(data, private_key):
# #     rsa_key = RSA.import_key(private_key)
# #     cipher = PKCS1_OAEP.new(rsa_key)
# #     return cipher.decrypt(b64decode(data)).decode()

# # API Endpoints
# @tool1.route('/encrypt', methods=['POST'])
# def encrypt():
#     data = request.json
#     print(f"Received data: {data}")  # Debug log to check the received data
    
#     # Check if 'key' is present in the incoming data
#     if 'key' not in data:
#         return jsonify({"error": "Key is missing in the request"}), 400
#     if 'text' not in data or 'method' not in data:
#         return jsonify({"error": "Text or method is missing in the request"}), 400
    
#     text = data['text']
#     key = data['key']
#     method = data['method']

#     try:
#         if method == "AES":
#             key = key[:16].encode()  # AES key must be 16 bytes
#             result = aes_encrypt(text, key)
#         elif method == "DES":
#             key = key[:8].encode()  # DES key must be 8 bytes
#             result = des_encrypt(text, key)
#         # elif method == "RSA":
#         #     private_key, public_key = generate_rsa_keys()
#         #     result = rsa_encrypt(text, public_key)
#         else:
#             return jsonify({"error": "Unsupported method"}), 400
        
#         return jsonify({"result": result})
#     except Exception as e:
#         print(f"Error during encryption: {str(e)}")  # Debug log
#         return jsonify({"error": str(e)}), 500

# @tool1.route('/decrypt', methods=['POST'])
# def decrypt():
#     data = request.json
#     print(f"Received data: {data}")  # Debug log to check the received data
    
#     # Check if 'key' is present in the incoming data
#     if 'key' not in data:
#         return jsonify({"error": "Key is missing in the request"}), 400
#     if 'text' not in data or 'method' not in data:
#         return jsonify({"error": "Text or method is missing in the request"}), 400
    
#     text = data['text']
#     key = data['key']
#     method = data['method']

#     try:
#         if method == "AES":
#             key = key[:16].encode()
#             result = aes_decrypt(text, key)
#         elif method == "DES":
#             key = key[:8].encode()
#             result = des_decrypt(text, key)
#         # elif method == "RSA":
#         #     result = rsa_decrypt(text, key)
#         else:
#             return jsonify({"error": "Unsupported method"}), 400
        
#         return jsonify({"result": result})
#     except Exception as e:
#         print(f"Error during decryption: {str(e)}")  # Debug log
#         return jsonify({"error": str(e)}), 500

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import string
import secrets

# Define the Blueprint for tool1
tool1 = Blueprint('tool1', __name__)

# Enable CORS for the blueprint
CORS(tool1)

# AES Encryption/Decryption
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return b64encode(cipher.iv + ciphertext).decode()

def aes_decrypt(data, key):
    raw = b64decode(data)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

# DES Encryption/Decryption
def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), DES.block_size))
    return b64encode(cipher.iv + ciphertext).decode()

def des_decrypt(data, key):
    raw = b64decode(data)
    iv, ciphertext = raw[:8], raw[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), DES.block_size).decode()

# Password Strength Checker
def check_password_strength(password):
    length_score = len(password) >= 12
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    score = sum([length_score, has_upper, has_lower, has_digit, has_special])
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    strength = strength_levels[score - 1]
    
    suggestions = []
    if not length_score:
        suggestions.append("Increase password length to at least 12 characters.")
    if not has_upper:
        suggestions.append("Add at least one uppercase letter.")
    if not has_lower:
        suggestions.append("Add at least one lowercase letter.")
    if not has_digit:
        suggestions.append("Include at least one digit.")
    if not has_special:
        suggestions.append("Use at least one special character (e.g., !@#$%^&*).")
    
    return {"strength": strength, "suggestions": suggestions}

# Generate Strong Password
def generate_strong_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(16))

# API Endpoints
@tool1.route('/password-strength', methods=['POST'])
def password_strength():
    data = request.json
    if 'password' not in data:
        return jsonify({"error": "Password is missing in the request"}), 400
    
    password = data['password']
    result = check_password_strength(password)
    return jsonify(result)

@tool1.route('/generate-password', methods=['GET'])
def generate_password():
    return jsonify({"password": generate_strong_password()})

@tool1.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    if 'key' not in data or 'text' not in data or 'method' not in data:
        return jsonify({"error": "Missing key, text, or method"}), 400
    
    text = data['text']
    key = data['key']
    method = data['method']
    
    try:
        if method == "AES":
            key = key.ljust(16)[:16].encode()
            result = aes_encrypt(text, key)
        elif method == "DES":
            key = key.ljust(8)[:8].encode()
            result = des_encrypt(text, key)
        else:
            return jsonify({"error": "Unsupported encryption method"}), 400
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@tool1.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    print(f"Received for decryption: {data}")  # Debug log
    
    if 'key' not in data or 'text' not in data or 'method' not in data:
        return jsonify({"error": "Missing key, text, or method"}), 400

    text = data['text']
    key = data['key']
    method = data['method']

    try:
        if method == "AES":
            key = key.ljust(16)[:16].encode()
            print(f"Using AES Key: {key}")  # Debug log
            result = aes_decrypt(text, key)
        elif method == "DES":
            key = key.ljust(8)[:8].encode()
            print(f"Using DES Key: {key}")  # Debug log
            result = des_decrypt(text, key)
        else:
            return jsonify({"error": "Unsupported decryption method"}), 400

        print(f"Decryption result: {result}")  # Debug log
        return jsonify({"result": result})
    except Exception as e:
        print(f"Decryption Error: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500
