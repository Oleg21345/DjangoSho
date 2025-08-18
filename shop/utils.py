from shop.models import Product, Order, OrderProduct, Customer, CouponForUser, BuyProduct


class CartForAuthUser:
    """Логіка Корзини"""

    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        if product_id and action:
            self.add_or_delete(product_id, action)


    def get_cart_info(self):
        """Отримання інформації про корзину"""
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        coupon_user, created = CouponForUser.objects.get_or_create(user=self.user)
        order_products = order.ordered.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            "order": order, # ID корзинки
            "order_products": order_products,  # QuerySet товарів в корзинці
            "quantity": cart_total_quantity, # Всю кількість товарів в корзинці
            "price": cart_total_price,  # Суму товарів корзинки
            "coupon_user": coupon_user
        }


    def add_or_delete(self, product_id, action):
        """Додавання або видалення продукту з корзини"""
        order = self.get_cart_info().get("order")
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == "add" and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        elif action == "delete":
            order_product.quantity -= 1
            product.quantity += 1
        elif action == "remove":
            product.quantity += order_product.quantity
            order_product.quantity -= order_product.quantity

        product.save()
        order_product.save()
        if order_product.quantity < 1:
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()["order"]
        order_products = order.ordered.all()
        for product in order_products:
            BuyProduct.objects.create(product=product)
        order.save()


def get_cart_data(request):
    """Вивід інформації в template"""
    cart = CartForAuthUser(request)
    cart_info = cart.get_cart_info()

    return {
        "order": cart_info.get("order"),
        "order_products": cart_info.get("order_products"),
        "cart_total_quantity": cart_info.get("quantity"),
        "cart_total_price": cart_info.get("price"),
        "coupon_user": cart_info.get("coupon_user")
    }






