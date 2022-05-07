from functools import wraps
import jwt 
from flask import * 

def token_required(secret):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('accessToken')
            if not token:
                return redirect('/login', 302)
            
            try:
                headers = jwt.get_unverified_header(token)
            except:
                return redirect('/login', 302)
            
            secret_key = secret

            if secret_key is None:
                return redirect('/login', 302)

            # Verify token is valid
            try:
                data = jwt.decode(token, secret_key, algorithms=['HS256'])
            except:
                return redirect('/login', 302)

            return f(*args, **kwargs)
        return decorated

    return decorator
