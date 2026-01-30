from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # required, login state is required

    def post(self, request):
        response = Response({
            "status": "success",
        })
        response.delete_cookie("refresh_token")
        return response
