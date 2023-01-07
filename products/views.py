from itertools import product
from unicodedata import category
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView

from products.models import Product,ProductQuestion
from products.forms import ProductForm

# Create your views here.
class ProductListView(ListView):
    """ List view for Product model"""
    model = Product
    template_name = "products/list.html"
    context_object_name = 'products'

    def get_queryset(self):
        keyword = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        queryset = []
        if keyword:
            queryset = Product.objects.filter(name__icontains=keyword)
        if category:
            queryset = queryset.filter(categories__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_val'] = self.request.GET.get('search', '')
        context['categories'] = Product.get_product_set_categories(
            context.get('products')
        )
        return context


class ProductDetailView(DetailView):
    """ Detail view for Product Model"""
    model = Product
    template_name = "products/detail.html"
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """ Create view for Product model"""
    model = Product
    template_name = "products/create.html"
    form_class = ProductForm

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

def ask_question(request, slug):
    if request.method == 'POST':
        if request.POST.get('question'):
            product = Product.objects.get(slug=slug)
            question_vals = {
                'question': request.POST.get('question'),
                'product': Product.objects.get(slug=slug),
                'questioner': request.user.profile,
                'responder': product.seller
            }
            question = ProductQuestion.objects.create(**question_vals)
    return redirect('products:detail', slug=slug)

def answer_question(request, slug, question_id):
    if request.method == 'POST':
        if request.POST.get('answer'):
            product = Product.objects.get(slug=slug)
            question = ProductQuestion.objects.get(
                pk=question_id,
                product=product,
            )
            if question:
                question.answer = request.POST.get('answer')
                question.save()
    return redirect('products:detail', slug=slug)