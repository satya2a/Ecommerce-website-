from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product


def _cart_items(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if not product:
            continue
        quantity = int(quantity)
        subtotal = product.price * quantity
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal

    return items, total


def home(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)

    categories = Product.objects.values_list("category", flat=True).distinct()
    return render(request, "store/home.html", {
        "products": products,
        "categories": [c for c in categories if c],
        "query": query,
        "selected_category": category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})


def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")

    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", slug=product.slug)

    cart = request.session.get("cart", {})
    current = int(cart.get(str(product_id), 0))
    if current >= product.stock:
        messages.warning(request, "You cannot add more than available stock.")
    else:
        cart[str(product_id)] = current + 1
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, f"{product.name} added to cart.")
    return redirect(request.POST.get("next") or "cart")


def update_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")

    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "Cart updated.")
    return redirect("cart")


def remove_from_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def cart_view(request):
    items, total = _cart_items(request)
    return render(request, "store/cart.html", {"items": items, "total": total})


@login_required
def checkout(request):
    items, total = _cart_items(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")

    initial = {
        "full_name": request.user.get_full_name() or request.user.username,
        "email": request.user.email,
    }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Re-check stock immediately before creating the order.
                for item in items:
                    product = Product.objects.select_for_update().get(id=item["product"].id)
                    if item["quantity"] > product.stock:
                        messages.error(request, f"Not enough stock for {product.name}.")
                        return redirect("cart")

                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    **form.cleaned_data,
                )

                for item in items:
                    product = Product.objects.select_for_update().get(id=item["product"].id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price=product.price,
                        quantity=item["quantity"],
                    )
                    product.stock -= item["quantity"]
                    product.save(update_fields=["stock"])

            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, f"Order #{order.id} placed successfully.")
            return redirect("orders")
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "store/checkout.html", {
        "form": form,
        "items": items,
        "total": total,
    })


@login_required
def orders(request):
    user_orders = request.user.orders.prefetch_related("items").all()
    return render(request, "store/orders.html", {"orders": user_orders})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})
