import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AuthResponse:
    def __init__(self, data):
        self.user = User(data.get("user", {})) if data.get("user") else None
        self.session = data if data.get("access_token") else None

class User:
    def __init__(self, data):
        self.id = data.get("id")
        self.email = data.get("email")

class SupabaseAuth:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

    def sign_in_with_password(self, credentials):
        email = credentials.get("email")
        password = credentials.get("password")
        
        # Ensure URL doesn't have trailing slash for consistency
        base_url = self.url.rstrip('/')
        
        try:
            url = f"{base_url}/auth/v1/token?grant_type=password"
            print(f"Attempting login to: {url}")
            r = requests.post(
                url,
                headers=self.headers,
                json={"email": email, "password": password}
            )
            
            if r.status_code != 200:
                print(f"Supabase Login Error: {r.status_code} - {r.text}")
                error_msg = "Login failed"
                try:
                    data = r.json()
                    error_msg = data.get("error_description") or data.get("msg") or data.get("message") or r.text
                    
                    if "Email not confirmed" in error_msg:
                        error_msg = "Email not confirmed. Please check your inbox for the verification link."
                    elif "rate limit" in error_msg.lower() or "too many" in error_msg.lower():
                        error_msg = "Too many attempts. Please wait a few minutes before trying again."
                except:
                    error_msg = r.text
                raise Exception(error_msg)
            
            return AuthResponse(r.json())
        except Exception as e:
            raise e

    def sign_up(self, credentials):
        email = credentials.get("email")
        password = credentials.get("password")
        options = credentials.get("options", {})
        data = options.get("data", {})
        
        base_url = self.url.rstrip('/')
        
        try:
            r = requests.post(
                f"{base_url}/auth/v1/signup",
                headers=self.headers,
                json={"email": email, "password": password, "data": data}
            )
            
            if r.status_code not in [200, 201]:
                error_msg = "Registration failed"
                try:
                    data = r.json()
                    error_msg = data.get("msg") or data.get("error_description") or data.get("message") or r.text
                    
                    if "rate limit" in error_msg.lower() or "too many" in error_msg.lower():
                        error_msg = "Too many attempts. Please wait a few minutes before trying again."
                except:
                    error_msg = r.text
                raise Exception(error_msg)
                
            return AuthResponse(r.json())
        except Exception as e:
            raise e

    def sign_out(self):
        # Stateless for the backend in this simple impl
        pass

class SupabaseClient:
    def __init__(self, url, key):
        self.auth = SupabaseAuth(url, key)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = None
if url and key and "YOUR_SUPABASE" not in url:
    try:
        supabase = SupabaseClient(url, key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found or invalid in environment variables.")
