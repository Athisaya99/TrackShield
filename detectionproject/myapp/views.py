from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group,User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from .models import *
from django .contrib .auth import login as auth_loginii
import  django.contrib.auth as auth
from django.contrib.auth import login as auth_login
def home(request):
    return render(request, 'index.html')


# def auth_login(request, user):
#     pass


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            auth_login(request,user)
            request.session['user_id']=user.id

            if user.groups.filter(name='admin'):
                return redirect('admin_index')

            elif user.groups.filter(name='locopilot'):
                locopilot=Locopilot.objects.get(USER=user)
                request.session['locopilot_id']=locopilot.id
                return redirect('locopilot_index')

            else:
                messages.error(request,'User does not belong to valid group')
                return redirect('login')

        else:
            messages.error(request,'invalid username or password ')
            return redirect('login')
    return  render(request,'login.html')


# ============================================================================================
@login_required
@never_cache
def admin_index(request):
    return render(request, 'admin_index.html')

@login_required
@never_cache
@csrf_exempt
def admin_add_locopilot(request):

    if request.method == 'POST':
        train_id = request.POST.get('train')
        name = request.POST.get('name')
        stationname = request.POST.get('stationname')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('admin_add_locopilot')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        group = Group.objects.get(name='Locopilot')
        user.groups.add(group)

        train = Train.objects.get(id=train_id)

        Locopilot.objects.create(
            USER=user,
            TRAIN=train,
            name=name,
            stationname=stationname,
            place=place,
            phone=phone,
            Email=email
        )

        messages.success(request, 'Registration successful.')
        return redirect('admin_add_locopilot')

    locopilots = Locopilot.objects.all()
    trains = Train.objects.all()

    return render(request, 'admin_add_locopilot.html', {
        'locopilots': locopilots,
        'trains': trains
    })

@login_required
@never_cache
def edit_locopilot(request, id):
    locopilot = get_object_or_404(Locopilot, id=id)

    if request.method == 'POST':
        train_id = request.POST.get('train')

        train = Train.objects.get(id=train_id)

        locopilot.TRAIN = train
        locopilot.name = request.POST.get('name')
        locopilot.stationname = request.POST.get('stationname')
        locopilot.place = request.POST.get('place')
        locopilot.phone = request.POST.get('phone')
        locopilot.Email = request.POST.get('email')

        locopilot.USER.username = request.POST.get('username')
        locopilot.USER.email = request.POST.get('email')
        locopilot.USER.save()

        locopilot.save()

        messages.success(request, 'Locopilot updated successfully.')
        return redirect('admin_add_locopilot')

    trains = Train.objects.all()

    return render(request, 'edit_locopilot.html', {
        'locopilot': locopilot,
        'trains': trains
    })


@login_required
@never_cache
def delete_locopilot(request, id):
    locopilot = Locopilot.objects.get(id=id)
    user=locopilot.USER
    user.delete()
    messages.success(request, 'Locopilot deleted successfully.')
    return redirect('admin_add_locopilot')



@login_required
@never_cache
def admin_camera(request):
    trains = Train.objects.all()

    if request.method == 'POST':
        train_id = request.POST.get('train')
        cameraname = request.POST.get('cameraname')

        if train_id and cameraname:
            train = Train.objects.get(id=train_id)
            Camera.objects.create(
                TRAIN=train,
                cameraname=cameraname,
            )
            messages.success(request, 'Camera added successfully.')
            return redirect('admin_camera')

    cameras = Camera.objects.all()
    return render(request, 'admin_camera.html', {
        'cameras': cameras,
        'trains': trains
    })


@login_required
@never_cache
def edit_camera(request, id):
    camera = get_object_or_404(Camera, id=id)
    trains = Train.objects.all()

    if request.method == 'POST':
        train_id = request.POST.get('train')
        cameraname = request.POST.get('cameraname')

        if train_id:
            camera.TRAIN = Train.objects.get(id=train_id)
        camera.cameraname = cameraname
        camera.save()

        messages.success(request, 'Camera updated successfully.')
        return redirect('admin_camera')

    return render(request, 'edit_camera.html', {
        'camera': camera,
        'trains': trains
    })


@login_required
@never_cache
def delete_camera(request, id):
    camera = get_object_or_404(Camera, id=id)
    camera.delete()
    messages.success(request, "deleted successfully.")
    return redirect('admin_camera')


@login_required
@never_cache
def admin_awareness(request):
    if request.method == "POST":
        Awareness.objects.create(
            # Get values from form
            title=request.POST.get("title"),
            message = request.POST.get("message"),
            priority = request.POST.get("priority"),
            date = request.POST.get("date"),
            time = request.POST.get("time"),
            status = request.POST.get("status"),
        )
        messages.success(request, "Notification Added Successfully")
        return redirect('admin_awareness')

    notifications = Awareness.objects.filter(status="Active").order_by('-date', '-time')
    return render(request, 'admin_awareness.html', {'notifications': notifications})


@login_required
@never_cache
def admin_history(request):
    alerts=Cameraalert.objects.all()
    return render(request, 'admin_history.html',{'alerts':alerts})


@login_required
@never_cache
def admin_complaint(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin_complaint.html', {'complaints': complaints})



@login_required
@never_cache
def admin_train(request):
    if request.method == 'POST':
        trainname = request.POST.get('trainname')
        trainnumber = request.POST.get('trainnumber')
        startingstation = request.POST.get('startingstation')
        endingstation = request.POST.get('endingstation')


        Train.objects.create(

            trainname=trainname,
            trainnumber=trainnumber,
            startingstation=startingstation,
            endingstation=endingstation,


        )

        messages.success(request, 'Registration successful.')
        return redirect('admin_train')

        # 🔥 VERY IMPORTANT PART
    trains = Train.objects.all()

    return render(request, 'admin_train.html', {
        'trains': trains
    })

@login_required
@never_cache
def edit_train(request, id):
    train = get_object_or_404(Train, id=id)

    if request.method == 'POST':
        train.trainname = request.POST.get('trainname')
        train.trainnumber = request.POST.get('trainnumber')
        train.startingstation = request.POST.get('startingstation')
        train.endingstation = request.POST.get('endingstation')

        train.save()

        messages.success(request, 'train updated successfully.')
        return redirect('admin_train')

    return render(request, 'edit_train.html', {'train': train})

@login_required
@never_cache
def delete_train(request, id):
    train = Train.objects.get(id=id)
    train.delete()
    messages.success(request, 'deleted successfully.')
    return redirect('admin_train')

def admin_logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect('login')



        # ====================================================================================
@login_required
@never_cache
def locopilot_index(request):
    return render(request, 'locopilot_index.html')

@login_required
@never_cache
def locopilot_live_Camera(request):
    locopilot = Locopilot.objects.get(USER=request.user)
    cameras = Camera.objects.filter(TRAIN=locopilot.TRAIN)
    return render(request, 'locopilot_live_Camera.html', {
        'cameras': cameras,
        'locopilot': locopilot
    })

@login_required
@never_cache
def locopilot_risk_level(request):
    return render(request, 'locopilot_risk_level.html')

@login_required
@never_cache
def locopilot_camera(request):
    return render(request, 'locopilot_camera.html')

@login_required
@never_cache
def locopilot_awareness(request):
    notifications = Awareness.objects.filter(status="active").order_by('-date', '-time')

    return render(request, 'locopilot_awareness.html', {'notifications': notifications})



from django.contrib.auth.decorators import login_required, login_required, login_required, login_required, \
    login_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Locopilot, Complaint


@login_required
@never_cache
def locopilot_complaint(request):
    try:
        # Get the logged-in locopilot
        locopilot = Locopilot.objects.get(USER=request.user)

    except Locopilot.DoesNotExist:
        messages.error(request, "")
        return redirect('locopilot_complaint')
    complaints=Complaint.objects.filter(LOCOPILOT__USER=request.user)

    if request.method == "POST":

        complaint_text = request.POST.get("complaint")
        date = request.POST.get("date")

        # Create complaint safely (no NULL foreign key)
        Complaint.objects.create(
            LOCOPILOT=locopilot,
            complaint=complaint_text,
            date=date
        )


        messages.success(request, "Complaint registered successfully.")
        return redirect('locopilot_complaint')

    return render(request, "locopilot_complaint.html",{'complaints':complaints})


@login_required
@never_cache
def admin_reply(request, id):
    complaint = get_object_or_404(Complaint, id=id)

    if request.method == "POST":
        reply_text = request.POST.get("reply")
        complaint.reply = reply_text
        complaint.save()
        messages.success(request, "Reply sent successfully.")
        return redirect('admin_complaint')   # Redirect only after POST

    return render(request, 'admin_reply.html', {'complaint': complaint})

@login_required
@never_cache
def edit_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)

    if request.method == "POST":
        complaint.complaint = request.POST.get('complaint')
        complaint.date = request.POST.get('date')
        complaint.save()
        return redirect('locopilot_complaint')

    return render(request, 'edit_complaint.html', {'complaint': complaint})

@login_required
@never_cache
def delete_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complaint.delete()
    return redirect('locopilot_complaint')



@login_required
@never_cache
def locopilot_history(request):
    loco=request.session['locopilot_id']
    alerts=Cameraalert.objects.filter(LOCOPILOT=loco)
    return render(request, 'locopilot_history.html',{'alerts':alerts})


def locopilot_logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect('login')
# =================================================================================

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import StreamingHttpResponse

from .models import Camera
from .core import new_detect_objects_high_risk as detector

@login_required
@never_cache
def detect_camera_view(request, camera_id):

    message = ""
    stream_url = request.session.get("stream_url")

    camera = Camera.objects.get(id=camera_id)

    if request.method == "POST":

        # START LIVE CAMERA
        if "start_camera" in request.POST:

            detector.RUN_DETECTION = True

            request.session["camera_id"] = camera.id

            stream_url = "/camera_stream/"
            request.session["stream_url"] = stream_url

            message = "Camera Detection Started"


        # STOP DETECTION
        if "stop_detection" in request.POST:

            detector.RUN_DETECTION = False

            request.session.pop("stream_url", None)

            return redirect("view_alert")


        # VIDEO DETECTION
        if "start_video" in request.POST:

            video_file = request.FILES["video_file"]

            fs = FileSystemStorage()

            filename = fs.save(video_file.name, video_file)

            video_path = fs.path(filename)

            request.session["video_path"] = video_path
            request.session["camera_id"] = camera.id

            detector.RUN_DETECTION = True

            stream_url = "/video_stream/"
            request.session["stream_url"] = stream_url

            message = "Video Detection Started"


    return render(request, "detect_camera.html", {
        "message": message,
        "stream_url": stream_url,
        "camera": camera
    })


def camera_stream(request):

    camera_id = request.session.get("camera_id")

    camera = Camera.objects.get(id=camera_id)

    return StreamingHttpResponse(
        detector.run_detection_stream(0, camera, None),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def video_stream(request):

    video_path = request.session.get("video_path")
    camera_id = request.session.get("camera_id")

    camera = Camera.objects.get(id=camera_id)

    return StreamingHttpResponse(
        detector.run_detection_stream(video_path, camera, None),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )



@login_required
@never_cache
def view_alert(request):

    locopilot = Locopilot.objects.get(USER=request.user)

    alerts = Cameraalert.objects.filter(
        CAMERA__TRAIN=locopilot.TRAIN
    ).order_by('-id')

    return render(request,'view_alert.html',{'alerts':alerts})

import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Gemini API Key
genai.configure(api_key="AIzaSyAFjM258hgf7_giqhUETUturRGTXqwtgOc")


@csrf_exempt
def locopilot_chatbot_api(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data.get("message", "").strip()

            if not message:
                return JsonResponse({"response": "Please type your question."})

            # ---------------- AI SYSTEM PROMPT ----------------
            system_instruction = """
You are Railway Safety AI Assistant for the Loco Pilot Module of the
Foreign Object Intrusion Detection System.

Your role is to help loco pilots understand system alerts, safety risks,
and railway track monitoring information.

You can answer questions about:
• Foreign object intrusion alerts
• Risk levels on railway tracks
• Animals, vehicles, debris, or people detected on tracks
• What actions a loco pilot should take
• How the detection system works
• Awareness notifications from admin
• How to report complaints
• How to view camera feeds and alerts

Rules:
• Keep answers short and clear.
• Use simple language.
• Give safety advice when needed.
• Focus only on railway safety and system usage.
• If the question is unrelated to railway safety, politely say you only answer railway safety questions.

Example answers:
If object detected → advise to slow down or alert control room.
If risk high → suggest emergency precaution.
"""

            final_prompt = f"{system_instruction}\n\nLoco Pilot Question: {message}\nAssistant:"

            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(final_prompt)
                response_text = response.text.strip()

            except Exception:
                response_text = "Sorry, the AI assistant is temporarily unavailable."

            return JsonResponse({"response": response_text})

        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid request format."}, status=400)

    return JsonResponse({"error": "POST request required"}, status=405)

def locopilot_chatbot_page(request):
    return render(request,"locopilot_chatbot.html")