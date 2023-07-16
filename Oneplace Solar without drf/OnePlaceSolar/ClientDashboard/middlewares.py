# """
# Created this file to logout the user once the Access Token is expired
# """

# from datetime import datetime
# from django.contrib.auth import logout
# from .models import ClientUsers
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


# class TokenExpirationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.user.is_authenticated:
#             print("Cheking if user is autheticated")
#             try:
#                 jwt_auth = JWTAuthentication()
#                 result = jwt_auth.authenticate(request)
#                 user = result[0] if result else None
#             except TokenError:
#                 user = None

#             if not user or not user.is_logged_in:
#                 # If the user is not authenticated or already logged out, no need to proceed
#                 return response

#             access_token_expiry = getattr(request.auth, 'exp', None)
#             print("Current toekn expires at :", access_token_expiry)
#             if access_token_expiry and datetime.utcnow().timestamp() > access_token_expiry:
#                 user.is_logged_in = False
#                 user.refresh_token = ''
#                 user.access_token = ''
#                 print(
#                     "The user is logged out because the Access token has expired please login again")
#                 user.save(update_fields=['is_logged_in',
#                           'refresh_token', 'access_token'])

#                 logout(request)

#         return response
