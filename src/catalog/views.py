from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views import View

from .models import Product, ProductSize
from .forms import UpdateForm, CreateForm

# Create your views here.

class ProductListView(ListView):
  template_name = 'catalog/index.html'
  model = Product
  
  def get_queryset(self, *args, **kwargs):
    return super(ProductListView, self).get_queryset(
        *args, **kwargs
    ).exclude(belongs_to=not self.request.user and not None)

class ProductCreateView(CreateView):
  template_name = 'catalog/create.html'
  model = Product
  fields = ['name']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = CreateForm()
    return context

  def post(self, *args, **kwargs):
    form = self.request.POST
    print(form)
    product_size, created = ProductSize.objects.get_or_create(
      width=form['product_size_width'],
      height=form['product_size_height'],
    )
    product = Product(
      name=form['name'],
      cut_file=self.request.FILES['cut_file'],
      belongs_to=self.request.user,
      product_size=product_size,
    )
    product.save()
    return redirect('catalog:index')

class ProductUpdateView(UpdateView):
  template_name = 'catalog/update.html'
  model = Product
  fields = ['name']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = UpdateForm({
      'name' :context['product'].name,
      # 'cut_file' :context['product'].cut_file,
      'product_size_width' :context['product'].product_size.width,
      'product_size_height' :context['product'].product_size.height,
    })
    return context


  # is_private = True
  # has_access = True

  # context = {
  #   'is_private': is_private,
  #   'has_access': has_access,
  # }
  # return render(request, 'catalog/update', context)
