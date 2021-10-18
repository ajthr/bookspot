def register_urls(app):

    from customers.views import (
        CustomerApiView,
        EmailAPIView,
        EmailSigninAPIView,
        GoogleSigninAPIView,
        LogoutAPIView,
        AddressAPIView
    )

    app.add_url_rule('/mail/',
                     view_func=EmailAPIView.as_view('send_mail'))
    app.add_url_rule('/email_signin/',
                     view_func=EmailSigninAPIView.as_view('email_signin'))
    app.add_url_rule('/google_signin/',
                     view_func=GoogleSigninAPIView.as_view('google_signin'))
    app.add_url_rule('/me/',
                     view_func=CustomerApiView.as_view('profile'))
    app.add_url_rule('/logout/',
                     view_func=LogoutAPIView.as_view('logout'))

    user_address_view = AddressAPIView.as_view('user_address')
    app.add_url_rule('/me/address/',
                     view_func=user_address_view, methods=["GET", "POST"])
    app.add_url_rule('/me/address/<int:id>/',
                     view_func=user_address_view, methods=["PATCH", "DELETE"])

    from products.views import (
        ProductsAPIView,
        ProductAPIView
    )

    app.add_url_rule('/books/',
                     view_func=ProductsAPIView.as_view('products'))
    app.add_url_rule('/books/<int:id>/',
                     view_func=ProductAPIView.as_view('product'))

    from staffs.views import (
        StaffAPIView,
        CreateStaffAPIView,
        StaffLoginAPIView,
        StaffLogoutAPIView,
        StaffChangePasswordAPIView,
        StaffResetPasswordAPIView,
        ManageProductsAPIView
    )

    app.add_url_rule('/staff/',
                     view_func=StaffAPIView.as_view('staff'))
    app.add_url_rule('/staff/create/',
                     view_func=CreateStaffAPIView.as_view('create_staff'))
    app.add_url_rule('/staff/login/',
                     view_func=StaffLoginAPIView.as_view('login_staff'))
    app.add_url_rule('/staff/logout/',
                     view_func=StaffLogoutAPIView.as_view('logout_staff'))
    app.add_url_rule('/staff/change_password/',
                     view_func=StaffChangePasswordAPIView.as_view('change_password_staff'))
    app.add_url_rule('/staff/reset_password/',
                     view_func=StaffResetPasswordAPIView.as_view('reset_password_staff'))

    manage_products_view = ManageProductsAPIView.as_view('manage_products')
    app.add_url_rule('/staff/products/',
                     view_func=manage_products_view, methods=["POST"])
    app.add_url_rule('/staff/products/<int:id>/',
                     view_func=manage_products_view, methods=["PATCH", "DELETE"])

    from cart.views import (
        CartItemAPIView
    )

    app.add_url_rule('/cart/',
                     view_func=CartItemAPIView.as_view('cart'))

    from orders.views import (
        OrderAPIView,
        OrdersAPIView,
        CreateOrderAPIView,
        ConfirmPaymentAPIView,
        CancelOrderAPIView
    )

    app.add_url_rule('/orders/',
                     view_func=OrdersAPIView.as_view('orders'))
    app.add_url_rule('/orders/<int:id>/',
                     view_func=OrderAPIView.as_view('order'))
    app.add_url_rule('/create_order/',
                     view_func=CreateOrderAPIView.as_view('create_order'))
    app.add_url_rule('/confirm_payment/',
                     view_func=ConfirmPaymentAPIView.as_view('confirm_payment'))
    app.add_url_rule('/cancel_order/',
                     view_func=CancelOrderAPIView.as_view('cancel_order'))
