from rest_framework import response, status, views, permissions
from account.models import User, UserAddress
from ..serializers import UserAddressSerializer
from utils import api_exception_handler

class UserAddressAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    @api_exception_handler
    def get(self, request):
        user: User = request.user
        
        user_address = UserAddress.objects.filter(user=user).prefetch_related()
        
        if user_address.exists():
            serializer = UserAddressSerializer(user_address, many=True)
            
            return response.Response({
                "status": "success",
                "message": f"User {user.username}'s all address found successfully",
                "results": serializer.data,
            }, status=status.HTTP_200_OK)
        
        
        return response.Response({
            "status": "error",
            "message": f"No address found for user {user.username}",
        }, status=status.HTTP_404_NOT_FOUND)
        
        
        