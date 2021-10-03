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
    app.add_url_rule('/me/address/',
                     view_func=AddressAPIView.as_view('address'))
    app.add_url_rule('/logout/',
                     view_func=LogoutAPIView.as_view('logout'))

    from products.views import (
        ProductsAPIView,
        ProductAPIView
    )

    app.add_url_rule('/books/',
                     view_func=ProductsAPIView.as_view('products'))
    app.add_url_rule('/books/<int:id>/',
                     view_func=ProductAPIView.as_view('product'))
