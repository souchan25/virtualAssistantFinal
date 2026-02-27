from rest_framework.throttling import SimpleRateThrottle

class AuthRateThrottle(SimpleRateThrottle):
    """
    Throttles authentication requests (login, register, etc)
    Uses 'auth' scope from settings.
    Throttles by IP address for anonymous users, and User ID for authenticated users.
    """
    scope = 'auth'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
