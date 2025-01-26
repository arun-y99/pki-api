from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from x509sign import generate_certificate

from pymongo import MongoClient

def generate_rsa_key_pair():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    public_key = private_key.public_key()

    return private_key, public_key

def save_keys_to_files(private_key, public_key, email):
    with open("keys/" + email + "_private_key.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open("keys/" +email+"_public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

if __name__ == "__main__":
    
    
    client = MongoClient('mongodb://localhost:27017')
    db = client['authentication']

    #Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair()
    save_keys_to_files(private_key, public_key, "admin")

    stored_key = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    
    cert = generate_certificate(stored_key.decode('utf-8'), private_key)

    admin_record = {"_id": "admin@pki.com", 
                    "name": "admin", 
                    "public_key": stored_key.decode('utf-8'),
                    "certificate": cert}

    db['pki'].insert_one(admin_record)
    print('Inserted admin record into the database.')
    



    
