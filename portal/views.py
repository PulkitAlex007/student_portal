from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def upload(request):
    return render(request,"upload.html")


from django.http import JsonResponse
from .models import studentdata


from django.http import JsonResponse
from .models import studentdata


def filter_students(request):

    center = request.GET.get("center")
    mode = request.GET.get("mode")
    caste = request.GET.get("caste")

    students = studentdata.objects.all()

    if center:
        students = students.filter(center_name=center)

    if mode:
        students = students.filter(mode=mode)

    if caste:
        students = students.filter(caste_category=caste)

    data = []

    for student in students:

        hours = student.course_hour

        # Course category logic
        if hours > 500:
            category = "B - Long Term Course"
        elif 90 <= hours <= 500:
            category = "C - Short Term Course"
        elif hours < 90:
            category = "D - Short Term Course"
        else:
            category = "E - DLC (CCC/CCC+/BCC)"

        data.append({
            "name": student.name,
            "course_name": student.course_name,
            "course_hour": student.course_hour,
            "course_category": category,
            "center_name": student.center_name,
            "mode": student.mode,
            "caste_category": student.caste_category,
        })
    
    return JsonResponse({"results": data})