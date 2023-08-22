from django.http import HttpResponseNotFound, JsonResponse
from rest_framework import status
from rest_framework.views import APIView


class ValidationBodyViewSet(APIView):
      def get(self, request):
        return JsonResponse({"mensaje":"test success"}, status=status.HTTP_200_OK)