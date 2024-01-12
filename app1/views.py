from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app1.models import *
from app1.serializer import PostModelSerializer, ChatMessageSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.
def indexPage(request):
    return render(request, 'Login/index.html')
def signupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        uemail = request.POST.get('email')
        upass = request.POST.get('password1')
        ucpass = request.POST.get('password2')
        if upass == ucpass:
            my_user = User.objects.create_user(first_name=fname,last_name=lname,email=uemail,password=upass,username=uname)
            my_user.save()
            messages.success(request,"Your account has been successfully created.")
            return redirect('login')
        else:
            return redirect('index')
    return render(request,'Login/signup.html')

# @login_required(login_url='signup')
def loginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('user_password')
        user = authenticate(request,username=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('base')
        else:
            messages.error(request, "Incorrect credentials")
            return redirect('login')
    return render(request,'Login/login.html')

# @login_required(login_url='login')

def basePage(request):
    return render(request,'Login/base.html')
# def logoutPage(request):
#     logout(request)
#     return redirect('index')
def logout_view(request):
    logout(request)
    return redirect('index')
def getpostPage(request):
    return render(request,'Post/get-post.html')
def helpPage(request):
    return render(request,'Post/help.html')
def postPage(request):
    return render(request,'Post/post.html')
def submit_form(request):
    return redirect('base')
def Post(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        passenger_name = request.POST.get('PassengerName')
        date_of_journey = request.POST.get('DateOfJourney')
        gender = request.POST.get('gender')
        flight_number = request.POST.get('FlightNumber')
        pnr_number = request.POST.get('PNRNumber')
        source = request.POST.get('source')  # Ensure field name consistency
        destination = request.POST.get('destination')  # Ensure field name consistency
        baggage_space = request.POST.get('BaggageSpace')
        checkbox = request.POST.get('checkbox') == 'on'  # Checkbox handling

        # Create a new instance of PostModel
        new_passenger = PostModel(
            passenger_name=passenger_name,
            date_of_journey=date_of_journey,
            gender=gender,
            flight_number=flight_number,
            pnr_number=pnr_number,
            source=source,
            destination=destination,
            baggage_space=baggage_space,
            is_checked=checkbox,
        )
        
        # Save the new instance to the database
        new_passenger.save()

    return render(request, 'Post/post.html', {})





class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        date_of_journey = self.request.query_params.get('date_of_journey', None)
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        gender = self.request.query_params.get('gender', None)
        flight_number = self.request.query_params.get('flight_number', None)
        if date_of_journey:
            qs =qs.filter(date_of_journey=date_of_journey)

        if source:
            qs =qs.filter(source=source)

        if destination:
            qs =qs.filter(destination=destination)

        if gender:
            qs =qs.filter(gender=gender)

        if flight_number:
            qs =qs.filter(flight_number=flight_number)
            
        # queryset = PostModel.objects.filter(date_of_journey=date_of_journey)
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







# class PostModelAPIView(generics.GenericAPIView):
#     serializer_class = PostModelSerializer
#     # queryset = PostModel.objects.all()
#     def get_queryset(self, request):
#         date_of_journey = self.kwargs['date_of_journey']
#         queryset = PostModel.objects.filter(date_of_journey=date_of_journey)
#         return queryset
#         # return Response(serializer.data, status=status.HTTP_200_OK)
#     # def post(self,request):
#     #     serializer = PostModelSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







class PostModelAPIViewID(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get_object(self,id):
        try:
            data = PostModel.objects.get(id=id)
            return data
        except PostModel.DoesNotExist:
            return None
    
    def get(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        qs = self.get_object(id)
        if qs is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        
        



#Chat views
    
 
@api_view(['GET', 'POST'])
def user_chat_list(request, user_id, other_user_id=None):
    if request.method == 'GET':
        # Retrieve all chatted users related to the user with ID user_id
        user_profiles = User.objects.exclude(userId=user_id)
        serializer = UserSerializer(user_profiles, many=True)
        return Response(serializer.data)
 
    elif request.method == 'POST':
        sender_profile = get_object_or_404(User, userId=user_id)
        receiver_profile = get_object_or_404(User, userId=other_user_id)
        serializer = ChatMessageSerializer(data=request.data)
 
        if serializer.is_valid():
            # Create a new chat message
            chat_message = serializer.save(sender=sender_profile, receiver=receiver_profile, timestamp=timezone.now())
 
            # Update user profiles with the new chat message
            sender_profile.chat_messages.add(chat_message)
            receiver_profile.chat_messages.add(chat_message)
 
            return Response(serializer.data, status=201)
 
        return Response(serializer.errors, status=400)
 
@api_view(['GET', 'POST'])
def chat_messages(request, user_id, other_user_id):
    if request.method == 'GET':
        # Retrieve chat messages between two users
        chat_messages = ChatMessage.objects.filter(
            Q(sender_id=user_id, receiver_id=other_user_id) | Q(sender_id=other_user_id, receiver_id=user_id)
        ).order_by('timestamp')
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)
 
    elif request.method == 'POST':
        sender_profile = get_object_or_404(User, userId=user_id)
        receiver_profile = get_object_or_404(User, userId=other_user_id)
        serializer = ChatMessageSerializer(data=request.data)
 
        if serializer.is_valid():
            # Create a new chat message
            chat_message = serializer.save(sender=sender_profile, receiver=receiver_profile)
 
            # Update user profiles with the new chat message
            sender_profile.chat_messages.add(chat_message)
            receiver_profile.chat_messages.add(chat_message)
 
            return Response(serializer.data, status=201)
 
        return Response(serializer.errors, status=400)
    

#filter condition

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import FilterModel
# from .serializer import FilterModelSerializer

# class FilteredPostAPIView(APIView):
#     # def get(self, request):
#     #     # Get all details from the FilterModel
#     #     all_details = FilterModel.objects.all()
#     #     serializer = FilterModelSerializer(all_details, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)

#     # def post(self, request):
#     #     # Deserialize the request data using the serializer
#     #     serializer = FilterModelSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         # Save the new entry to the FilterModel
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def get(self, request):
#         # Filter posts where destination is 'HelpDesk'
#         filtered_posts = FilterModel.objects.filter(destination='helpPage')
#         serializer = FilterModelSerializer(filtered_posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#rating
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserRating
from .serializer import UserRatingSerializer

class UserRatingAPIView(APIView):
    def post(self, request):
        serializer = UserRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
