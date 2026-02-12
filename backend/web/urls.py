from django.urls import path, re_path

from web.views.create.character.create import CreateCharacterView
from web.views.create.character.get_list import GetListCharacterView
from web.views.create.character.get_single import GetSingleCharacterView
from web.views.create.character.remove import RemoveCharacterView
from web.views.create.character.update import UpdateCharacterView
from web.views.homepage.index import HomepageIndexView
from web.views.index import index
from web.views.profile.update import UpdateProfileView
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.register import RegisterView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.get_user_info import GetUserInfoView

# 从上往下顺序匹配
urlpatterns = [
    # 后端路由
    path('api/user/account/login/', LoginView.as_view()), # api/ used to avoid conflict with frontend route
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),

    path('api/create/character/create/', CreateCharacterView.as_view()),
    path('api/create/character/remove/', RemoveCharacterView.as_view()),
    path('api/create/character/update/', UpdateCharacterView.as_view()),
    path('api/create/character/get_single/', GetSingleCharacterView.as_view()),

    path('api/create/character/get_list/', GetListCharacterView.as_view()),

    path('api/homepage/index/', HomepageIndexView.as_view()),
    path('', index),

    # 兜底路由，所有前端的非media开头的页面，都返回index页面
    # 因为index页面定义了RouterView，然后访问router/index.js, 从而加载的前端页面
    re_path(r'^(?!media/|static/|assets/).*$', index)
]
