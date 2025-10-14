from src.service.auth.auth_service import AuthService


def test_decode_encode_password():
    original_password = "6789Nikita!Nik" 
    
    hashpassword = AuthService().create_hastpassword(original_password)
    encode_password = AuthService().verify_password(original_password, hashpassword)
    
    assert encode_password