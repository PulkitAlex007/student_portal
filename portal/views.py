from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
from .forms import StudentDataForm

from .forms import ExcelUploadForm
# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")




def upload(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            # Read Excel into DataFrame
            df = pd.read_excel(excel_file)

            # Loop through each row and save using ModelForm
            for _, row in df.iterrows():
                data = {
                    'session': row.get('session'),
                    'name': row.get('name'),
                    'course_name': row.get('course_name'),
                    'course_hour': row.get('course_hour'),
                    'scheme': row.get('scheme'),
                    'mode': row.get('mode'),
                    'caste_category': row.get('caste_category'),
                    'center_name': row.get('center_name'),
                    'trained': row.get('trained', False),
                    'certified': row.get('certified', False),
                    'placed': row.get('placed', False),
                }
                StudentDataForm(data).save()

            return redirect('upload_excel')  # Redirect back or anywhere you want
    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})


def filter_data(request):
    query = request.GET.get("q")


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
