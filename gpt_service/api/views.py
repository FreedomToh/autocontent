from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class MakeRequestApi(APIView):

    def post(self, request, **kwargs):
        print("ok")
        return Response(status=status.HTTP_200_OK)
