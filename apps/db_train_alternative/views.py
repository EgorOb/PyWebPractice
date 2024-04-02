from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Author


class AuthorREST(View):
    def get(self, request, id=None):

        if id is None:
            for author in Author.objects.all():
                pass
        else:
            data = get_object_or_404(Author, id=id)


        return JsonResponse(list(data.values()), safe=False, json_dumps_params={"ensure_ascii": False,
                                                       "indent": 4})


# Create your views here.
