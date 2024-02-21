from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject,Feedback
from django.contrib.auth.forms import PasswordChangeForm
import logging

logger = logging.getLogger(__name__)

def subjects_adder(request):
    if request.method == "POST":
        numOfSubjects=int(request.POST.get('num_subjects'))
        
        for i in range (numOfSubjects):
            nameOfSub=request.POST.get(f'subject_name_{i+1}')
            classesAtt=request.POST.get(f'classes_attended_{i+1}')
            classesDone=request.POST.get(f'classes_done_{i+1}')
            subject = Subject(
                user=request.user,  # Assuming user is logged in
                name=nameOfSub,
                classes_attended=classesAtt,
                classes_done=classesDone
            )
            subject.save()
        return redirect('home')
    return render(request, 'main/subjectsAdder.html')

@login_required
def index(request):
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'main/index2.html', {'subjects': subjects})
    # return HttpResponse('heelo')

def login_view(request):
    if request.method == 'POST':
        # Handling login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            return redirect('home/')  # Redirect to home page upon successful login
        else:
            # Authentication failed, you can handle this case (e.g., display an error message)
            return HttpResponse('Authentication failed')

    # If it's a GET request, render the login page
    return render(request, 'main/login.html')

def handlesignup(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # checks
        if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Please choose a different one.')
                return render(request, 'main/signup.html')
        elif(password!=password2):
            messages.error(request, 'Password confirmation doesn\'t match password')
            return render(request, 'main/signup.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
            return render(request, 'main/signup.html')

        # create user
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        login(request, myuser)
        return redirect('add_subjects')
    return render(request, 'main/signup.html')

@login_required
def log_attendance(request, subject_id):
    subject = Subject.objects.get(id=subject_id)

    if request.method == "POST":
        attended = request.POST.get('attended')

        if attended == 'yes':
            # User attended the lecture, update both classes_done and classes_attended
            subject.classes_done += 1
            subject.classes_attended += 1
        elif attended == 'no':
            # User did not attend the lecture, only update classes_done
            subject.classes_done += 1

        subject.save()
        return redirect('home')  # Redirect to home page after updating

    return render(request, 'main/log_attendance.html', {'subject': subject})

@login_required
def support_page(request):
    return render(request, 'main/support_page.html')

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback', '')
        # Process the feedback (e.g., store it in a database)
        return redirect('home')
    else:
        return HttpResponse('Invalid request method')

@login_required   
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'main/change_password.html', {'form': form})

@login_required
def create_new_table(request):
    if request.method == 'POST':
        # Logic to delete the current table (assuming you want to delete all subjects for the user)
        Subject.objects.filter(user=request.user).delete()

        # Logic to create a new table based on the submitted form data
        num_subjects = int(request.POST.get('num_subjects'))

        for i in range(num_subjects):
            name_of_sub = request.POST.get(f'subject_name_{i+1}')
            classes_att = request.POST.get(f'classes_attended_{i+1}')
            classes_done = request.POST.get(f'classes_done_{i+1}')

            subject = Subject(
                user=request.user,
                name=name_of_sub,
                classes_attended=classes_att,
                classes_done=classes_done
            )
            subject.save()

        messages.success(request, 'New table created successfully!')
        return redirect('home')

    return render(request, 'main/create_new.html')

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')  # Retrieve feedback from the form

        if feedback_text:  # Check if feedback text is not empty
            # Save the feedback to the database
            feedback = Feedback.objects.create(content=feedback_text)
            return JsonResponse({'message': 'Feedback submitted successfully'})
        else:
            return JsonResponse({'error': 'Feedback content is empty'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)