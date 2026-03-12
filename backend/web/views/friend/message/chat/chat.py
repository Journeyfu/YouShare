from langchain_core.messages import HumanMessage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend
from web.views.friend.message.chat.graph import ChatGraph


class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()
        if not message:
            return Response({
                'result': "message can not be empty"
            })
        # pk: primary key 作用等于 id
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': "friend does not exist"
            })
        friend = friends.first()
        app = ChatGraph.create_app()

        inputs = {
            'messages': [HumanMessage(message)]
        }
        res = app.invoke(inputs)
        print(res['messages'][-1].content) # List: 0: human messages 1: ai messages
        return Response({
            'result': 'success'
        })