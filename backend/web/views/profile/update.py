from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.views.utils.photo import remove_old_photo


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            # get 返回1个元素，如果有多个或0个会报错
            # filter 返回列表
            user_profile = UserProfile.objects.get(user=user)
            username = request.data.get('username').strip()
            profile = request.data.get('profile').strip()[:500] # 长度截断
            photo = request.FILES.get('photo', None)

            if not username:
                return Response( {
                    'result': 'username is empty'
                })

            if not profile:
                return Response( {
                    'result': 'profile is empty'
                })
            if username != user.username and User.objects.get(username=username).exists():
                return Response({
                    'result': 'username is taken'
                })

            if photo:
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo
            user_profile.profile = profile
            user_profile.update_time = now()
            user_profile.save()
            user.username = username
            user.save()
            return Response( {
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url,
            })

        except:
            return Response(
                {'result', 'system error, try later'}
            )