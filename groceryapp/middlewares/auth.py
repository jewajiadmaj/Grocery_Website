from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

def auth_middleware(get_response):
    def middleware(request):
        if not request.session.get('customer_id'):
            returnUrl = request.META['PATH_INFO']
            print(returnUrl)  # Debug: Check what URL is causing the issue
            login_url = reverse('loginc')  # Use reverse to avoid hardcoding URLs
            query_string = urlencode({'return_url': returnUrl})
            redirect_url = f'{login_url}?{query_string}'
            return redirect(redirect_url)

        response = get_response(request)
        return response

    return middleware
