from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.urls import reverse

from .models import FileUpload, Upload, STRUCT



class UploadIndexView(ListView):
  model = Upload
  template_name = 'upload/index.html'
  context_object_name = 'files'

  def get_context_data(self, *args, **kwargs):
    ctx = super().get_context_data(*args, **kwargs)
    ctx['partners'] = User.objects.filter(
      is_superuser=False, is_staff=False)
    # ctx['files'] = UploadedFile.objects.filter(
    #   upload_method='MANUAL',
    # )
    return ctx


  def post(self, *args, **kwargs):
    partner = self.request.POST.get('partner')

    try:
      csv_file = self.request.FILES["file"].file.read().decode(
          'utf-8-sig').splitlines()
    except MultiValueDictKeyError:
      print('TODO')
      return render(self.request, 'upload/index.html')

    doc = FileUpload(file=self.request.FILES['file'])
    doc.save()
    try:
      header_descriptor = doc.process_csv_header(csv_file)
    except Exception as e:
      return HttpResponse('Empty file', status=400)
    carts = doc.process_csv_body(csv_file, header_descriptor, partner, self.request)
    print(carts)
    return redirect(reverse('index',
      # kwargs={ 'carts': carts, 'payment': payment, },
    ))
    