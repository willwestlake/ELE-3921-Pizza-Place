from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Pizza, Drink, Topping, Order
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

def menu_view(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()
    toppings = Topping.objects.all()

    return render(request, 'menu/menu.html', {
        'pizzas': pizzas,
        'drinks': drinks,
        'toppings': toppings,
    })

def add_to_cart(request):
    if request.method == 'POST':
        pizza_id = request.POST.get('pizza_id')
        topping_ids = request.POST.getlist('toppings')
        drink_ids = request.POST.getlist('drinks')

        pizza = get_object_or_404(Pizza, id=pizza_id)
        valid_toppings = Topping.objects.filter(id__in=topping_ids, size=pizza.size)
        selected_drinks = Drink.objects.filter(id__in=drink_ids)

        cart = request.session.get('cart', [])
        cart.append({
            'pizza_id': pizza.id,
            'topping_ids': [str(t.id) for t in valid_toppings],
            'drink_ids': [str(d.id) for d in selected_drinks]
        })
        request.session['cart'] = cart

        return redirect('menu')

def cart_view(request):
    cart = request.session.get('cart', [])
    cart_items = []
    cart_total = 0

    for item in cart:
        try:
            pizza = Pizza.objects.get(id=item['pizza_id'])
            toppings = Topping.objects.filter(id__in=item['topping_ids'])
            drinks = Drink.objects.filter(id__in=item.get('drink_ids', []))

            toppings_total = sum(t.price for t in toppings)
            drinks_total = sum(d.price for d in drinks)
            total_price = pizza.price + toppings_total + drinks_total
            cart_total += total_price

            cart_items.append({
                'pizza_type': pizza.name,
                'size': pizza.size.name,
                'pizza_price': pizza.price,
                'toppings': [{'name': t.name, 'price': t.price} for t in toppings],
                'toppings_total': toppings_total,
                'drinks': [{'name': d.name, 'size': d.size, 'price': d.price} for d in drinks],
                'drinks_total': drinks_total,
                'total_price': total_price,
            })
        except Exception as e:
            print(f"Cart error: {e}")
            continue

    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def remove_from_cart(request):
    index = int(request.POST.get('index'))

    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        del cart[index]
        request.session['cart'] = cart

    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total_price = 0

    for item in cart:
        try:
            pizza = Pizza.objects.get(id=item['pizza_id'])
            toppings = Topping.objects.filter(id__in=item['topping_ids'])

            toppings_price = sum(t.price for t in toppings)
            item_total = pizza.base_price + toppings_price

            total_price += item_total

            cart_items.append({
                'pizza': pizza,
                'toppings': toppings,
                'item_total': item_total
            })

        except Pizza.DoesNotExist:
            continue

    return render(request, 'menu/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@require_POST
def remove_from_cart(request):
    index = int(request.POST.get('index'))
    cart = request.session.get('cart', [])
    
    if 0 <= index < len(cart):
        cart.pop(index)
        request.session['cart'] = cart

    return HttpResponseRedirect(reverse('cart'))

@login_required
def checkout_view(request):
    cart = request.session.get('cart', [])

    for item in cart:
        try:
            pizza = Pizza.objects.get(id=item['pizza_id'])
            toppings = Topping.objects.filter(id__in=item['topping_ids'])
            drinks = Drink.objects.filter(id__in=item.get('drink_ids', []))

            order = Order.objects.create(
                user=request.user,
                pizza=pizza,
                size=pizza.size
            )
            order.topping.set(toppings)
            order.drink.set(drinks)
        except Exception as e:
            print(f"Checkout error: {e}")
            continue

    request.session['cart'] = []  # Clear cart
    return render(request, 'menu/checkout_success.html')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at',"-id")
    return render(request, 'menu/profile.html', {'orders': orders})

def reorder_view(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        cart = request.session.get('cart', [])

        cart.append({
            'pizza_id': order.pizza.id,
            'topping_ids': [t.id for t in order.topping.all()],
            'drink_ids': [d.id for d in order.drink.all()]
        })

        request.session['cart'] = cart
        return redirect('cart')




