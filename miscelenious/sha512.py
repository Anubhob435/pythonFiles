import hashlib

def compute_sha256(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()

def compute_sha512(message: str) -> str:
    return hashlib.sha512(message.encode()).hexdigest()

if __name__ == "__main__":
    text = "Hello, world"
    sha256_result = compute_sha256(text)
    sha512_result = compute_sha512(text)

    print("SHA256:", sha256_result)
    print("SHA512:", sha512_result)