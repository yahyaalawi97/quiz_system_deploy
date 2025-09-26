from django.shortcuts import render, redirect ,get_object_or_404
from .models import User , Question , Quiz , result
from django.contrib import messages 
import bcrypt
from django.http import JsonResponse

#log in 
def login(request):
    if request.method == "POST":
            email = request.POST.get("login_email")
            password = request.POST.get("login_password")
            try :
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode(),user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    messages.error(request, "Invalid email or password!")
            except User.DoesNotExist:
                 messages.error(request, "Invalid email or password!")

    return render(request, "log_in_page.html")
#registration ************************
def register (request):
    if request.method =="POST":
            errors = User.objects.basic_validator(request.POST)
            if errors:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('register')

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=hashed_pw
                )
                messages.success(request, "Registration successful!")
                return redirect('register')
    return render(request , "register_page.html" )
#logout *****************************
def logout(request):
    request.session.flush()
    return redirect('login')
#home **************************
def home(request):
     
     user_id = request.session.get('user_id')
     if not user_id:
        return redirect('login')  
     user = User.objects.get(id=user_id)

     quizzes = Quiz.objects.all()   
     context = {
        "user": user,
        "quizzes": quizzes
                 }
     return render(request, 'home.html', context)
#about us 
def about_us (request):
     return render (request , "about_us.html")
#creation ***********************
def create_quiz(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        if not any(key.endswith("_text") for key in request.POST.keys()):
            return JsonResponse({"success": False, "errors": {"questions": "You must add at least one question"}})

        if len(title) < 3:
            return JsonResponse({"success": False, "errors": {"title": "Title too short"}})

        quiz = Quiz.objects.create(
            title=title,
            desc=desc,
            created_by=user,
        )

        question_count = 0
        for key in request.POST:
            if key.startswith("q") and key.endswith("_text"):
                question_count += 1
                q_text = request.POST.get(f"q{question_count}_text")
                q_type = request.POST.get(f"q{question_count}_type")

                if q_type == "mcq":
                    options = [
                        request.POST.get(f"q{question_count}_option1"),
                        request.POST.get(f"q{question_count}_option2"),
                        request.POST.get(f"q{question_count}_option3"),
                        request.POST.get(f"q{question_count}_option4"),
                    ]
                    #to make it [0-3] insted [1-4]
                    correct_index = int(request.POST.get(f"q{question_count}_correct")) - 1
                    correct = options[correct_index]
                elif q_type == "tf":
                    options = ["True", "False"]
                    correct = request.POST.get(f"q{question_count}_correct")
                else:
                    options = []
                    correct = request.POST.get(f"q{question_count}_correct", "")

                Question.objects.create(
                    quiz=quiz,
                    question_text=q_text,
                    question_type=q_type,
                    options=options if options else None,
                    correct_answer=correct
                )

        return JsonResponse({"success": True})

    return render(request, "create_quiz.html", {"user": user})

#editing ************************
def editquiz (request , quiz_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    try:
        quiz = Quiz.objects.get(id=quiz_id, created_by=user)
    except Quiz.DoesNotExist:
        messages.error(request, "Quiz not found or you don't have permission!")
        return redirect('home')
    question = Question.objects.filter(quiz = quiz)
    if request.method == "POST":
        quiz.title = request.POST.get("title")
        quiz.desc = request.POST.get("desc")
        quiz.save()

        for i , question in enumerate(question , start = 1):
            q_text = request.POST.get(f"q{i}_text")
            q_type = request.POST.get(f"q{i}_type")
            correct = request.POST.get(f"q{i}_correct")

            question.question_text = q_text
            question.question_type = q_type
            question.correct_answer = correct

           
            if q_type == "mcq":
                options = []
                j = 0
                while True:
                    option_key = f"q{i}_option{j+1}"
                    if option_key in request.POST:
                        options.append(request.POST[option_key])
                        j += 1
                    else:
                        break
                question.options = options
            else:
                question.options = None  

            question.save()

            return redirect ("home")


    context = {
        "user" : user , 
        "question" : question ,
        "quiz" : quiz,
    }
    return render (request , "edit_quiz.html" , context)
#delete *************************
def deletequiz(request , quiz_id):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)
    print("quiz_id:", quiz_id)
    print("user:", user)
    print("All quizzes by this user:", Quiz.objects.filter(created_by=user))
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=user)
    
    
    quiz.delete()
    
    messages.success(request, "Quiz deleted successfully!")
    return redirect('home')
#ing quiz ***********************
def doquiz(request , quiz_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    quiz = get_object_or_404(Quiz , id=quiz_id)
    question = Question.objects.filter(quiz = quiz)
    context = {
        "user" : user , 
        "question" : question ,
        "quiz" : quiz,
    }

    return render (request , "do_quiz.html" , context)


     