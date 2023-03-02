from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q

from apps.products.models import Product,ProductQuestion, Brand, ProductReview
from apps.products.forms import ProductForm, AttributeFormSet, ProductReviewForm
from apps.orders.models import OrderLine
from apps.notifications.models import Notification
from apps.notifications.mixins import NotificationMixin
# Create your views here.
class ProductListView(NotificationMixin, ListView):
    """ List view for Product model"""
    model = Product
    template_name = "products/list.html"
    context_object_name = 'products'

    def get_queryset(self):
        keyword = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        queryset = Product.objects.exclude(
            Q(seller=self.request.user.profile) | Q(stock_qty=0)
        )
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(brand__name__icontains=keyword)
            )
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


class ProductDetailView(NotificationMixin, DetailView):
    """ Detail view for Product Model"""
    model = Product
    template_name = "products/detail.html"
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.exclude(
            Q(seller=self.request.user.profile) | Q(stock_qty=0)
        )


class ProductCreateView(LoginRequiredMixin, NotificationMixin, CreateView):
    """ Create view for Product model"""
    model = Product
    template_name = "products/create.html"
    form_class = ProductForm
    formset_class = AttributeFormSet
    success_url = reverse_lazy('users:my-profile')

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        if self.request.POST:
            context['formset'] = AttributeFormSet(self.request.POST)
        else:
            context['formset'] = AttributeFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save()
        formset = AttributeFormSet(self.request.POST)
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(form)

@login_required
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
            Notification.send_notification(
                sender=request.user.profile,
                receiver=product.seller,
                title=f'New question on product: {product}',
                message=f'Question: "{question.question}"',
                url=reverse_lazy('users:questions')
            )
    return redirect('products:detail', slug=slug)

@login_required
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
                Notification.send_notification(
                sender=request.user.profile,
                receiver=question.questioner,
                title=f'New answer on product: {product}',
                message=f'Answer: "{question.answer}"',
                url=reverse_lazy('products:detail', kwargs={'slug': product.slug})
            )
    return redirect('users:questions')

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.user.profile.shopping_cart
    cart.add_item(product)
    return redirect('users:cart:cart')

class ProductReviewCreateView(LoginRequiredMixin, NotificationMixin, CreateView):
    model = ProductReview
    template_name = "products/reviews/add.html"
    form_class = ProductReviewForm
    success_url = reverse_lazy('users:my-profile')

    def get_context_data(self, **kwargs):
        context = super(ProductReviewCreateView, self).get_context_data(**kwargs)
        context['order_line'] = get_object_or_404(
            OrderLine,
            pk=self.kwargs['pk']
        )
        return context

    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['order_line'] = get_object_or_404(
            OrderLine,
            pk=self.kwargs['pk']
        )
        kwargs['reviewer'] = self.request.user.profile
        return kwargs