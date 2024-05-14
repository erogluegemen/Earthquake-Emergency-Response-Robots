from django.views.decorators import gzip
from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
from django.core.files.base import ContentFile
from django.http import HttpResponse

import datetime
from .models import *
from .utils.camera_utils import VideoCamera, gen
from .utils.dataframe_utils import create_dataframe_from_model
from .utils.microphone_utils import initialize_stream, plot_generator, close_stream

def home(request):
    return render(request, 'home.html')

@gzip.gzip_page
def camera_stream(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass    
    return render(request, 'camera_stream.html')

def control_panel(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'Move Forward':
            print('1')
        elif action == 'Move Backward':
            print('2')
        elif action == 'Turn Right':
            print('3')
        elif action == 'Turn Left':
            print('4')
    return render(request, 'control_panel.html')

def visualize_sound(request):
    p, stream = initialize_stream()
    image_data = plot_generator(stream)
    return render(request, 'sound_wave_visualization.html', {'image_data': image_data})

def preview_data(request):
    html_table = None
    if request.method == 'POST':
        model_name = request.POST.get('model')
        if model_name:
            model = globals().get(model_name)
            if model:
                html_table = create_dataframe_from_model(model=model)
            else:
                html_table = None
                
    context = {'html_table':html_table}
    return render(request, 'preview_data.html', context=context)

def take_picture(request):
    if request.method == 'GET':
        cam = VideoCamera()
        frame = cam.get_frame()
        picture = Picture()
        picture.image.save(f'detected_person_{datetime.datetime.now()}.jpg', ContentFile(frame), save=True)
        
        return redirect('control_panel')
    else:
        return HttpResponse('Method not allowed!')
    
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def system_architecture(request):
    return render(request, 'system_architecture.html')
