def cart_context(request):
    cart = request.session.get("cart", {})
    cart_count = sum(int(qty) for qty in cart.values())
    return {"cart_count": cart_count}
