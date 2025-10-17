from auth_utils import hash_password, verify_password, create_token, decode_token

def test_password_hash_roundtrip():
    pwd = 'Secret123!'
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)


def test_token_encode_decode():
    token = create_token(1, 'user', 15)
    payload = decode_token(token)
    assert payload
    assert payload['username'] == 'user'
    assert payload['age'] == 15
