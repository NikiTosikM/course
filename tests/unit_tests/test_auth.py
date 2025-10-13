from datetime import datetime, timedelta, timezone
from src.service.auth.auth_service import AuthService



def test_create_hashpassword():
    hashpassword = AuthService().create_hastpassword("6789Nikita!Nik")
    
    assert hashpassword
    assert isinstance(hashpassword, str)
    

def test_create_decode_access_token():
    user_id = 1
    encoded_jwt = AuthService().create_access_token(user_id)
    decode_data = AuthService().decode_token(encoded_jwt)
    
    assert decode_data["user_id"] == user_id