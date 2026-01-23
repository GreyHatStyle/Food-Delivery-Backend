from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class AnonBurstRateThrottle(AnonRateThrottle):
    scope = 'anon_burst'