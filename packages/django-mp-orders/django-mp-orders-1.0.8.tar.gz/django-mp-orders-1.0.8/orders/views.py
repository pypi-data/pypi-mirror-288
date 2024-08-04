import json

from django.apps import apps
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from orders import utils
from orders.constants import ORDER_STATUS_NEW
from orders.models import Order
from orders.forms import CheckoutForm


@transaction.atomic
def checkout(request):

    user = request.user
    initial = {'mobile': '+380'}

    if user.is_authenticated:
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name
        })

    form = CheckoutForm(
        initial=initial,
        data=request.POST or None
    )

    if request.method == 'POST' and form.is_valid():

        cart = request.cart

        order = form.save(commit=False)

        order.status_id = ORDER_STATUS_NEW

        order.address = '%s, %s' % (
            form.cleaned_data['warehouse'],
            form.cleaned_data['city']
        )

        if user.is_authenticated:
            order.user = request.user

        order.save()

        for item in cart.items:
            ordered_product = order.items.create(
                qty=item.qty,
                **item.product.get_order_attrs())

            if apps.is_installed('clothes'):
                request.clothes.create_size(ordered_product)

        cart.clear()

        utils.send_new_order_notifications(request, order)

        return redirect('orders:success', order.hash)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'serialized_products': [
            item.product.serialize() for item in request.cart.items
        ]
    })


def success(request, order_hash):

    order = get_object_or_404(Order, hash=order_hash)

    products = request.products.filter(
        id_in=order.items.values_list('product_id', flat=True)
    )

    context = {
        'order': order,
        'serialized_products': [
            product.serialize() for product in products
        ]
    }

    callback_url = request.build_absolute_uri(reverse('home'))

    if hasattr(request, 'liqpay') and order.is_paynow_form_visible():
        context['checkout_form'] = request.liqpay.get_checkout_form(
            amount=order.total,
            order_id=order.id,
            description=_('Products sale'),
            result_url=callback_url,
            server_url=callback_url,
            language=request.LANGUAGE_CODE
        )

    return render(request, 'orders/success.html', context)


@staff_member_required
def resend_new_order_notifications(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    utils.send_new_order_notifications(request, order)
    return HttpResponse('Message sent')


@staff_member_required
def render_new_order_email(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = utils.get_new_order_context(order)
    context['debug'] = True
    return render(request, 'orders/new_order_email_for_manager.html', context)


@login_required
def get_history(request):
    context = {'order_items': request.user.order.all()}
    return render(request, 'orders/history.html', context)
