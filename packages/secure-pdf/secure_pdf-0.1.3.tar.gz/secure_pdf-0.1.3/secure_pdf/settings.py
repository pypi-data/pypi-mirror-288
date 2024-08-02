from pydantic import BaseModel

class settings:
    title:str = "Secure PDF Documents"
    allowed: list[str] = ["pdf"]
    upload_msg: str = "Please upload a pdf file"
    default_password : str = "123456"
    password_suggestion_msg: str = f"Please enter a password. The password must be at least 5 characters long. default Password is "
    password_decrypt_suggestion_msg: str = f"Please enter password of uploade PDF "
    password_input_msg: str = "Enter password for file"
    download_file_msg: str = "Download protected PDF"
    application_type: str = "application/pdf"
    no_file_msg: str = "No file uploaded yet"
    image_url: str = "https://cdn.pixabay.com/photo/2022/05/20/18/24/lock-7209995_1280.png"

class server_settings:
    port:str = "8000"
    
