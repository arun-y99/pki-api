# pki-api
A public-key infrastructure system using Django that performs key management and certificate verification

---

## Features
- Generate 2048-bit RSA key pairs for public-key cryptography operations like public-key encryption and digital signatures.
- Submit a Certificate Signing Request (CSR) form for storing public key in the database.
- Verify the validity of the certificate.

---

## Endpoints and Scripts

### 1. Generating keys

First, an admin key pair must be generated. This can be done by running
```bash
python3 pki/main/adminkeygen.py
```
This will add the admin public key to the database.

### 2. Submit CSR form

**Endpoint:**\
`POST /register`

**Description:**\
Creates a new entry for the submitted public key and generates an X.509 certificate.

**Request Body (JSON):**

```json
{
  "email": email,
  "name": name,
  "public_key": <contents of the .pem file>
}
```
**Response (JSON):**

- **Successful registration**
  ```json
  {
    "name": name,
    "email": email,
    "certificate'" cert
  }
  ```
  The success page will be displayed.
- **Failed verification**
  The failure page will be displayed.

---

### 3. Verify Certificate

**Endpoint:**\
`POST /verify`

**Description:**\
For a given certificate, verify if the certificate is valid or not.

**Request Body (JSON):**

```json
{
  "email": email,
  "cert": <contents of the certificate file>
}
```
**Response (JSON):**

- **Successful**
  ```json
  {
    "email": email
  }
  ```
  The success page will be displayed.
- **Failure**
   The failure page will be displayed.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install Django.

3. Install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

4. Generate an admin key pair by running
   ```bash
   python3 adminkeygen.py
   ```
   
   
5. Run the application:
   ```bash
   python3 manage.py runserver
   ```

---

## Disclaimer

This project is for demonstration purposes only and is not designed for production. It should not be used in production environments or for critical applications.

---

