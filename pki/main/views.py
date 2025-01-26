import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import UploadForm, VerifyForm

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from pymongo import MongoClient

from .X509certificate import generate_certificate,verify_certificate_signature

client = MongoClient('mongodb://localhost:27017')
db = client['authentication']

# Create your views here.


def index(request):
    return render(request, 'index.html')

def CSR(request):
    return render(request, 'CSR.html', { "form": UploadForm() })

def certificate(request):
    return render(request, 'certificate.html', {"form": VerifyForm()})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        
        form = UploadForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            user_stored_key = form.cleaned_data['public_key']

            #print(public_key_file)
            if not (email and name and user_stored_key):
                return JsonResponse({'error': 'No file uploaded'}, status=400)

            # user_public_key = serialization.load_pem_public_key(open(public_key_file, "rb").read())

            # user_stored_key = user_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

            # admin_record = db['pki'].find_one({"_id": "admin@pki.com"})

            check_record = db['pki'].find_one({"public_key": user_stored_key})
            if check_record:
                return render(request, 'registered_failure.html')

            admin_private_key = serialization.load_pem_private_key(open("/Users/ysarun/Projects/PKI/pki/main/keys/admin_private_key.pem", "rb").read(), password=None)

            cert = generate_certificate(user_stored_key, admin_private_key)

            user_record = {"_id": email, 
                            "name": name,
                            "public_key": user_stored_key,
                            "certificate": cert}

            try:
                db['pki'].insert_one(user_record)
                return render(request, 'registered_success.html', {'name': name, 'email': email, 'certificate': cert})
            except Exception:
                form = UploadForm()
                return render(request, 'registered_failure.html')
    return render(request, 'index.html', {'form': form})
        
def verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        email = form.data['email']
        user_record = db['pki'].find_one({"_id": email})
        if not user_record:
            return render(request, 'verify_failure.html')
        
        #user_certificate = user_record['certificate']
        user_certificate = form.data['cert']
        if verify_certificate_signature(user_certificate, serialization.load_pem_public_key(open("/Users/ysarun/Projects/PKI/pki/main/keys/admin_public_key.pem", "rb").read())):
            return render(request, 'verified_success.html', {'email': email})
        else:
            form = VerifyForm()
            return render(request, 'verified_failure.html')
        