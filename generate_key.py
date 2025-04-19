import hashlib

SECRET_KEY = "c0nc3rt-secret"

def generate_key(client_id):
    return hashlib.sha256((client_id + SECRET_KEY).encode()).hexdigest()

if __name__ == "__main__":
    print(generate_key("valid-client-"))