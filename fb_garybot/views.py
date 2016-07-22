from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse


class GaryBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'thisisgarysecretbot':
            return HttpResponse(self.request.GET['hub.challenge'])
        return HttpResponse("100460735")