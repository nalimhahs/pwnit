from rest_framework.views import APIView
from rest_framework.response import Response
from scrapper.tasks import add_movie


class add_movie_api_view(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            add_movie.delay(data=request.data)
            return Response({"message": "success"})
        except Exception as err:
            print(err)
            return Response({"error": "An error occured"}, status=400)
