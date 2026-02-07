from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# F5 刷新不会自动调用这个api，调用位置在api.js里，当登录响应状态失败的时候会重新申请refreshtoken，用到了这个
class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({"result": "refresh token is not exists"}, status=401)
            else:
                refresh = RefreshToken(refresh_token) # auto-detect if outdated, if yes, then raise Exception
                if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
                    refresh.set_jti()
                    response = Response({
                        'result': 'success',
                        'access': str(refresh.access_token),
                    })

                    response.set_cookie(
                        key='refresh_token',
                        value=str(refresh),
                        httponly=True,
                        samesite='Lax',
                        secure=True,
                        max_age=86400 * 7,
                    )
                    return response

                return Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                })

        except:
            return Response({
                "result": "refresh token outdated"
            }, status=401) # 401 is required