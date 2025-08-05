import hashlib

password = "mypassword"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(hash_value)
