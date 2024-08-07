from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

userModel = get_user_model()

class ShopifyAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            from user._verify_shopify_token import verify_shopify_jwt
            is_valid, payload = verify_shopify_jwt(request.META['HTTP_AUTHORIZATION'].split(' ')[-1], settings.SHOPIFY_SECRET_KEY)
            if is_valid:
                try:
                    print(payload['dest'][8:], payload['sub'])
                    user = userModel.objects.get(name=payload['dest'][8:])
                except userModel.DoesNotExist:
                    shop = payload['dest'][8:]
                    email = shop+'@shopify.com'
                    user = userModel.objects.create(name=shop, email=email, shopify_user=True)
                    user.name = shop
                    user.save()
                request.user = user
                print(request.user.id)
                from django.contrib.auth import login
                login(request, user,'user.auth.AuthBackend')
        