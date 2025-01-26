from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_certificate(message, private_key):
    """
    Generate an X.509 certificate for a given message.

    Parameters:
        message (str): The message to include in the certificate.
        key_length (int): The length of the RSA key in bits. Default is 2048.

    Returns:
        tuple: A tuple containing the private key and certificate as PEM strings.
    """

    # Generate certificate subject and issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Tamil Nadu"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Chennai"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])

    # Build certificate
    certificate = x509.CertificateBuilder()
    certificate = certificate.subject_name(subject)
    certificate = certificate.issuer_name(issuer)
    certificate = certificate.public_key(private_key.public_key())
    certificate = certificate.serial_number(x509.random_serial_number())
    certificate = certificate.not_valid_before(datetime.now())
    certificate = certificate.not_valid_after(datetime.now() + timedelta(days=365))  # Valid for 1 year

    # Add custom extension with the message
    certificate = certificate.add_extension(
        x509.SubjectAlternativeName([x509.DNSName(message)]), critical=False
    )

    # Sign certificate with the private key
    certificate = certificate.sign(private_key, hashes.SHA256(), default_backend())

    # Serialize keys and certificate
    private_key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    ).decode('utf-8')

    certificate_pem = certificate.public_bytes(Encoding.PEM).decode('utf-8')

    return certificate_pem

def verify_certificate_signature(certificate_pem, public_key):
    """
    Verifies the signature of an X.509 certificate.

    Parameters:
        certificate_pem (str): The PEM-encoded certificate to verify.
        public_key: The public key of the issuer for verification.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    try:
        # Load the certificate
        certificate = x509.load_pem_x509_certificate(certificate_pem.encode('utf-8'), default_backend())

        # Verify the certificate's signature
        public_key.verify(
            certificate.signature,                    # The certificate's signature
            certificate.tbs_certificate_bytes,       # The 'to-be-signed' portion of the certificate
            padding.PKCS1v15(),                      # Padding used
            hashes.SHA256()                                 # Hash algorithm used
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False