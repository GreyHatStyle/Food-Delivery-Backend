from django.utils import timezone

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle
from typing import TypedDict

class UserThrottleStatusType(TypedDict):
    attempts: int
    last_attempt_time: float
    

class LoginThrottle(BaseThrottle):
    """
    Login Custom Ratelimiting class for not allowing users to login after defined
    wrong attempts
    """
    scope = 'login_scope'

    def get_cache_key(self, request):
        ident = self.get_ident(request)
        return f'login_attempt_{ident}', f'login_throttled_{ident}'
    
    def set_cache(self, key: str, data: UserThrottleStatusType, timeout: int = 86400):
        """
        Sets cache for User throttle, may add additional logs and features for this function that's why user defined
        """
        cache.set(
            key=key,
            value=data,
            timeout=timeout
        )
        return
    
    def get_cache(self, key: str) -> UserThrottleStatusType:
        """
        Gets cache for User throttle, may add additional logs and features for this function that's why user defined
        """
        data: UserThrottleStatusType = cache.get(
            key=key,
            default={
                'attempts': 1,
                'last_attempt_time': 0,
            }
        )
        return data
    
    def set_throttle(self, key: str, throttled_time_seconds: int | float):
        """
        Sets User to throttle state for `throttled_time_seconds` seconds.
        """
        cache.set(
            key=key,
            value="Throttled",
            timeout=throttled_time_seconds,
        )
    
    def is_throttled(self, key_throttled: str) -> bool:
        """
        Check if user is throttled or not, and returns time for how much time it is.
        """
        
        # this ttl() is supported by 'redis' that's why its working
        exp_time = cache.ttl(key_throttled)
        
        if exp_time > 0:
            self.wait_time = exp_time
            return True
        
        return False

    
    def allow_request(self, request, view):
        if request.method != "POST":
            return True
        
        key, key_throttled = self.get_cache_key(request)
        
        if self.is_throttled(key_throttled):
            return False
        
        user_throttle_status = self.get_cache(key)
        attempts = user_throttle_status['attempts']
        last_attempt_time = user_throttle_status['last_attempt_time']
        current_time = timezone.now().timestamp()
        
        
        print("ENTERED THE LOGIN THROTTLE CLASS TO CHECK, ATTEMPTS: ", attempts)
        
        self.set_cache(
            key=key,
            data={
                'attempts': attempts+1,
                'last_attempt_time': current_time, 
            },
        )

        if attempts == 1:
            return True


        if attempts < 3:
            return True
            
        
        # Rate limit for 1 min
        elif attempts == 3:
            time_elapsed = current_time - last_attempt_time
            self.wait_time = 60 - time_elapsed
            self.set_throttle(key_throttled, self.wait_time)
            return False
        
        
        # Afterwards all the 3rd wrong attempts will be throttled for 5 mins
        elif attempts % 3 == 0:
            time_elapsed = current_time - last_attempt_time
            self.wait_time = 300 - time_elapsed
            self.set_throttle(key_throttled, self.wait_time)
            return False
            


        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        return self.wait_time
    
    
    
    # Methods to be used outside the class by APIView
    def clear_throttles(self, request):
        """
        clears all login cache related to this request
        """
        key, key_throttled = self.get_cache_key(request)
        cache.delete(key)
        cache.delete(key_throttled)
        return
    
    def get_attempts_left(self, request):
        """
        Current attempts left for this particular request
        """
        key, _ = self.get_cache_key(request)
        data = self.get_cache(key)
        return 3 - ((int(data['attempts'])-1) % 3)
        