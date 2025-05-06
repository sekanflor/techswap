from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
import time

def rate_limit(requests=100, window=60):
    """
    Rate limiting decorator that limits the number of requests per window period.
    
    Args:
        requests (int): Maximum number of requests allowed in the window period
        window (int): Time window in seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance, request, *args, **kwargs):
            # Get client IP address
            client_ip = request.META.get('REMOTE_ADDR')
            
            # Create a unique key for this client
            cache_key = f'rate_limit_{client_ip}'
            
            # Get current request count and window start time
            current = cache.get(cache_key)
            
            if current is None:
                # First request in the window
                cache.set(cache_key, {
                    'count': 1,
                    'window_start': time.time()
                }, window)
            else:
                # Check if we're still in the same window
                if time.time() - current['window_start'] > window:
                    # Reset window
                    cache.set(cache_key, {
                        'count': 1,
                        'window_start': time.time()
                    }, window)
                else:
                    # Increment count
                    current['count'] += 1
                    cache.set(cache_key, current, window)
                    
                    # Check if limit exceeded
                    if current['count'] > requests:
                        return JsonResponse(
                            {
                                'error': 'Rate limit exceeded',
                                'message': f'Too many requests. Please try again in {int(window - (time.time() - current["window_start"]))} seconds.'
                            },
                            status=429
                        )
            
            # Call the original view function
            return view_func(view_instance, request, *args, **kwargs)
        return wrapped_view
    return decorator 