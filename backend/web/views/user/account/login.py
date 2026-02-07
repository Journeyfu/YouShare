from django.contrib.admin.templatetags.admin_modify import change_form_object_tools_tag
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username").strip()
            password = request.data.get("password").strip()

            if not username or not password:
                return Response({"result": "username or password is required"})

            user = authenticate(username=username, password=password)
            if user: # username and password are matched
                user_profile = UserProfile.objects.get(user=user) # 从数据库读信息
                refresh = RefreshToken.for_user(user) # generate jwt 得到一对access和refresh token

                # access token
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
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

            else:
                return Response({"result": "username or password is wrong"})

        except:
            return Response({
                'result': "system error, try later."
            })
