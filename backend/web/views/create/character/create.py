from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.models.user import UserProfile


class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get('name').strip()
            profile = request.data.get('profile').strip()[:100000]
            photo = request.data.get('photo', None)
            background_image = request.data.get('background_image', None)
            if not name:
                return Response({'result': 'Name is required'})
            if not profile:
                return Response({'result': 'Profile is required'})
            if not photo:
                return Response({'result': 'Photo is required'})
            if not background_image:
                return Response({'result': 'Background image is required'})
            Character.objects.create(
                name=name,
                profile=profile,
                photo=photo,
                background_image=background_image
            )
            return Response({'result': 'Character created successfully'})

        except:
            return Response({'result': 'system error, try later'})

