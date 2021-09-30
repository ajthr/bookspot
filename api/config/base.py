from flask import Response
from flask.views import MethodView


class BaseView(MethodView):

    def get(self):
        return Response(status=405)

    def post(self):
        return Response(status=405)

    def put(self):
        return Response(status=405)

    def patch(self):
        return Response(status=405)
