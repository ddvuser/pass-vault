from django.core import signing

def encrypt(raw_str: str, encryption_key: str) -> str:

    signer = signing.Signer(salt=encryption_key)
    return signer.sign_object(raw_str)


def decrypt(encoded_str: str, encryption_key: str) -> str:

    signer = signing.Signer(salt=encryption_key)
    try:
        return signer.unsign_object(encoded_str)
    except signing.BadSignature:
        raise ValueError(f"Unable to decode hash {encoded_str}")