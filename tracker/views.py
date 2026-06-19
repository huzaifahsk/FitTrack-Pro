from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Workout, Diet, WeightProgress, ProgressPhoto
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def home(request):
    return render(request, 'tracker/home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, 'tracker/signup.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, 'tracker/login.html')


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    total_workouts = Workout.objects.filter(user=request.user).count()
    total_meals = Diet.objects.filter(user=request.user).count()
    total_photos = ProgressPhoto.objects.filter(user=request.user).count()

    latest_weight = WeightProgress.objects.filter(
        user=request.user
    ).order_by("-date").first()

    weights = WeightProgress.objects.filter(
        user=request.user
    ).order_by("date")

    weight_dates = [str(w.date) for w in weights]
    weight_values = [w.weight for w in weights]

    return render(request, 'tracker/dashboard.html', {
        "total_workouts": total_workouts,
        "total_meals": total_meals,
        "total_photos": total_photos,
        "latest_weight": latest_weight,
        "weight_dates": weight_dates,
        "weight_values": weight_values,
    })


@login_required
def workout(request):
    if request.method == "POST":
        exercise = request.POST.get("exercise")
        sets = request.POST.get("sets")
        reps = request.POST.get("reps")

        Workout.objects.create(
            user=request.user,
            exercise=exercise,
            sets=sets,
            reps=reps
        )

        return redirect("workout")

    workouts = Workout.objects.filter(user=request.user).order_by("-date")
    return render(request, 'tracker/workout.html', {"workouts": workouts})


@login_required
def delete_workout(request, id):
    workout = Workout.objects.get(id=id, user=request.user)
    workout.delete()
    return redirect("workout")


@login_required
def diet(request):
    if request.method == "POST":
        food_name = request.POST.get("food_name")
        calories = request.POST.get("calories")
        protein = request.POST.get("protein")

        Diet.objects.create(
            user=request.user,
            food_name=food_name,
            calories=calories,
            protein=protein
        )

        return redirect("diet")

    diets = Diet.objects.filter(user=request.user).order_by("-date")
    return render(request, 'tracker/diet.html', {"diets": diets})


@login_required
def delete_diet(request, id):
    meal = Diet.objects.get(id=id, user=request.user)
    meal.delete()
    return redirect("diet")


@login_required
def weight(request):
    if request.method == "POST":
        weight_value = request.POST.get("weight")

        WeightProgress.objects.create(
            user=request.user,
            weight=weight_value
        )

        return redirect("weight")

    weights = WeightProgress.objects.filter(user=request.user).order_by("-date")
    return render(request, 'tracker/weight.html', {"weights": weights})


@login_required
def delete_weight(request, id):
    weight = WeightProgress.objects.get(id=id, user=request.user)
    weight.delete()
    return redirect("weight")


@login_required
def photos(request):
    if request.method == "POST":
        photo = request.FILES.get("photo")

        ProgressPhoto.objects.create(
            user=request.user,
            photo=photo
        )

        return redirect("photos")

    photos = ProgressPhoto.objects.filter(user=request.user).order_by("-date")
    return render(request, 'tracker/photos.html', {"photos": photos})


@login_required
def delete_photo(request, id):
    photo = ProgressPhoto.objects.get(id=id, user=request.user)
    photo.delete()
    return redirect("photos")

@login_required
def bmi(request):
    bmi_value = None
    category = None

    if request.method == "POST":
        height = float(request.POST.get("height"))
        weight = float(request.POST.get("weight"))

        height_meter = height / 100
        bmi_value = weight / (height_meter * height_meter)
        bmi_value = round(bmi_value, 2)

        if bmi_value < 18.5:
            category = "Underweight"
        elif bmi_value < 25:
            category = "Normal Weight"
        elif bmi_value < 30:
            category = "Overweight"
        else:
            category = "Obese"

    return render(request, 'tracker/bmi.html', {
        "bmi_value": bmi_value,
        "category": category
    })

@login_required
def download_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FitTrack_Report.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "FitTrack Pro Report")

    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"User: {request.user.username}")

    y -= 30

    workouts = Workout.objects.filter(user=request.user)
    diets = Diet.objects.filter(user=request.user)
    latest_weight = WeightProgress.objects.filter(user=request.user).order_by('-date').first()

    p.drawString(50, y, f"Total Workouts: {workouts.count()}")
    y -= 20

    p.drawString(50, y, f"Total Meals: {diets.count()}")
    y -= 20

    if latest_weight:
        p.drawString(50, y, f"Latest Weight: {latest_weight.weight} kg")

    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Workout History")

    y -= 25

    p.setFont("Helvetica", 10)

    for workout in workouts:
        p.drawString(
            50,
            y,
            f"{workout.exercise} | Sets: {workout.sets} | Reps: {workout.reps}"
        )
        y -= 15

    y -= 20

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Diet History")

    y -= 25

    p.setFont("Helvetica", 10)

    for diet in diets:
        p.drawString(
            50,
            y,
            f"{diet.food_name} | Calories: {diet.calories} | Protein: {diet.protein}g"
        )
        y -= 15

    p.save()

    return response

@login_required
def report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fitness_report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Fitness Report - {request.user.username}")

    workouts = Workout.objects.filter(user=request.user).count()
    meals = Diet.objects.filter(user=request.user).count()
    photos = ProgressPhoto.objects.filter(user=request.user).count()

    latest_weight = WeightProgress.objects.filter(
        user=request.user
    ).order_by("-date").first()

    p.drawString(100, 750, f"Total Workouts: {workouts}")
    p.drawString(100, 720, f"Total Meals: {meals}")
    p.drawString(100, 690, f"Progress Photos: {photos}")

    if latest_weight:
        p.drawString(
            100,
            660,
            f"Latest Weight: {latest_weight.weight} kg"
        )

    p.save()
    return response