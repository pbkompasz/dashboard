from django.shortcuts import render
from django.views.generic.detail import BaseDetailView
from django.views import View

from .mixins import JSONResponseMixin
from upload.models import UploadedFile

# Create your views here.

class JSONDetailView(JSONResponseMixin, View):
  model = UploadedFile

  def render_to_response(self, context, **response_kwargs):
    return self.render_to_json_response(context, **response_kwargs)

  

