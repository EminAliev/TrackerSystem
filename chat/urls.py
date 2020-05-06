from django.urls import path

from chat.views import ChatView, CreateMessageView, MessageView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('add/', CreateMessageView.as_view(), name='add'),
    path('entry/', MessageView.as_view(), name='typing'),
]
