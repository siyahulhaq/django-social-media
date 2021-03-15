from rest_framework import response,views

# Create your views here.

class ProfileView(views.APIView):
    def get(self, request, *args, **kwargs):
        return response.Response({'data':'test_data'})