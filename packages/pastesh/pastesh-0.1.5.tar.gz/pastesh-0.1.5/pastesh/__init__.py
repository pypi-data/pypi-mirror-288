import os
import subprocess
import tempfile
import base64
import requests
from hashlib import sha512

def randbase64(length):
    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8').rstrip('=')

def writekey(id, serverkey, clientkey):
    return f"{id}{serverkey}{clientkey}https://paste.sh"

def encrypt_message_openssl(message, id, serverkey, clientkey, header, version=3):
    if version == 3 and "Subject: " in header:
        subject = header.replace("Subject: ", "").replace("\n", "")
        if subject:  # Only add subject if it is not empty
            message = f"Subject: {subject}\n\n{message}"
        else: 
            message = f" {message}"
    key = writekey(id, serverkey, clientkey).encode()
    key = sha512(key).digest()[:32]  # AES-256 key
    
    # Create a temporary file to hold the plaintext message
    with tempfile.NamedTemporaryFile(delete=False) as tmp_plain_file:
        tmp_plain_file.write(message.encode())
        tmp_plain_file_path = tmp_plain_file.name
    
    # Create a temporary file to hold the encrypted message
    with tempfile.NamedTemporaryFile(delete=False) as tmp_enc_file:
        tmp_enc_file_path = tmp_enc_file.name
    
    # Encrypt the message using OpenSSL
    subprocess.run([
        "openssl", "enc", "-aes-256-cbc", "-md", "sha512", "-pass", f"pass:{writekey(id, serverkey, clientkey)}", 
        "-iter", "1", "-base64", "-in", tmp_plain_file_path, "-out", tmp_enc_file_path
    ], check=True)
    
    # Read the encrypted message
    with open(tmp_enc_file_path, 'r') as enc_file:
        encrypted_message = enc_file.read()
    
    # Clean up temporary files
    os.remove(tmp_plain_file_path)
    os.remove(tmp_enc_file_path)
    
    return encrypted_message

def upload_to_pastesh(title, message, api_endpoint="https://paste.sh", version=3):
    serverkey = randbase64(18)
    id = randbase64(6)
    clientkey = randbase64(18)
    header = f"Subject: {title}" if title else ""

    encrypted_message = encrypt_message_openssl(message, id, serverkey, clientkey, header, version)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(encrypted_message.encode())
        tmp_file_path = tmp_file.name

    try:
        with open(tmp_file_path, 'rb') as f:
            response = requests.put(f"{api_endpoint}/{id}", headers={
                "X-Server-Key": serverkey,
                "Content-type": "text/vnd.paste.sh-v3"
            }, data=f)
            response.raise_for_status()

        return f"{api_endpoint}/{id}#{clientkey}"

    finally:
        os.remove(tmp_file_path)

# # Example usage
# if __name__ == "__main__":
#     title = "Sample Title"  # Set to an empty string or None if no title is desired
#     message = "This is the body of the paste."
#     api_endpoint = "https://paste.sh"
    
#     try:
#         url = upload_to_pastesh(title, message, api_endpoint)
#         print(f"Paste created successfully: {url}")
#     except Exception as e:
#         print(f"Failed to create paste: {str(e)}")

