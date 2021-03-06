import json

from channels import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, CreateView, View

from chat.models import Chat, Message


class ChatView(LoginRequiredMixin, TemplateView):
    """Просмотр чата"""
    template_name = 'chat/page.html'

    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data()
        if Chat.objects.count():
            context['messages'] = Chat.objects.first().messages.all()
        else:
            room = Chat.objects.create()
            room.users.add(self.request.user)
        return context


class CreateMessageView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""
    model = Message
    fields = ['text', 'chat', 'sender']

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message', None)
        sender = int(request.POST.get('sender', None))
        if message and sender:
            new_message = Message.objects.create(
                chat=Chat.objects.first(),
                sender=User.objects.get(pk=sender),
                text=message
            )
            args = {'message': new_message}
            recipient_message = render_to_string('chat/message_other.html', args)
            sender_message = render_to_string('chat/message_in.html', args)

            Group("room").send({
                "text": json.dumps({
                    "recipient_message": recipient_message,
                    "sender_message": sender_message,
                    "sender": self.request.user.pk
                })
            })

            return JsonResponse(
                dict(recipient_message=recipient_message,
                     sender_message=sender_message)
            )
        return HttpResponse('')


class MessageView(View):
    """Просмотр сообщения"""

    def post(self, request, *args, **kwargs):
        user_pk = self.request.POST.get('user', 0)
        user = User.objects.get(pk=user_pk)
        Group("room").send({
            "text": json.dumps({
                'action': 'typing',
                'user': user_pk,
                'username': user.username
            }),
        })

        return HttpResponse("Hello, test")
