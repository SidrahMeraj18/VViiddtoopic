from email import message
from re import S
from django.shortcuts import redirect, render, reverse
import os
import youtube_dl 
from django.conf import settings
import subprocess as sp
from whoosh_index_and_search_file_content import srtsearch
from .models import Srtgen, Favourites
from moviepy.editor import *
from icecream import ic
from django.contrib import messages
from users.models import AuthUser
from django.http.response import HttpResponse
import mimetypes
from mimetypes import MimeTypes
from urllib.request import pathname2url
from django.http import HttpResponse
def uploadlink(request):
    if request.method=="POST":
        print(request.POST["link"])
        videofolder=os.path.join(str(settings.BASE_DIR),"videos")
        os.chdir(videofolder)
        filename=request.user.username+'_'+str(request.user.id)+'_'+request.POST["title"]
        # try:
        url = request.POST["link"]
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename+".mp4"
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        file_location = os.path.join(str(settings.BASE_DIR) , "videos" ,filename+".mp4")
        file_location1 = os.path.join(str(settings.BASE_DIR) , "previews" ,filename+".mp4")
        clip=VideoFileClip(file_location)
        theDuration = clip.duration
        # getting subclip
        clip = clip.subclip(0, 10)
        previewoutput=file_location1
        clip.write_videofile(previewoutput)
        ic(request.POST.getlist('public'))
        theObject = Srtgen.objects.create(user=request.user.authuser,title=request.POST["title"], link=request.POST["link"], public=True if len(request.POST.getlist('public')) != 0 else False, duration=theDuration)
        os.chdir("..")
        from django.core.files import File
        # save preview and video in theObject
        theObject.preview.save(filename+".mp4", File(open(file_location1, 'rb')))
        theObject.video.save(filename+".mp4", File(open(file_location, 'rb')))
        theObject.save()
        theObject.save()
        os.remove(file_location1)
        MODEL_SCRIPT_PATH = os.path.join(str(settings.BASE_DIR),"py-srt-generator")
        print(file_location)
        args = [
        "python", 
        f"{MODEL_SCRIPT_PATH}/run.py", 
        file_location,
        f"{filename}.srt",
        ]
        print(" ".join(args))
        logs = sp.run(args)
        print(logs)
        with open(f'{MODEL_SCRIPT_PATH}\\{filename}.srt', 'r') as f:
            file = f.read().split('\n')
            new_text = "<br>".join(file)
            print(file)
        with open(f"{MODEL_SCRIPT_PATH}\\{filename}.srt", 'rb') as fi:
            theObject.file = File(fi, name=os.path.basename(filename+".srt"))
            theObject.save()
        return redirect(reverse("preview", kwargs={"srt_id": theObject.id }))
    context={}
    return render(request,"uploadLink.html",context)
search_hwe_results = []
def previewvideo(request,srt_id):
    obj=Srtgen.objects.get(id=srt_id)
    a=obj.file.url
    print(a , "ppp")
    aname=os.path.basename(a)
    f = open(obj.file.path,'r')
    srt_content = f.read()
    f.close()
    context={"obj":obj,"pathsrt":aname,"srt":srt_content }
    if request.method=="POST":
        ic(request.user.is_authenticated)
        if request.user.is_authenticated == True:
            val=request.POST["key"]
            v=val.split(",")
            if len(val) != 0:
                appendd=str(settings.BASE_DIR)+str(a)
                print(appendd,"hahha")
                ic(str(appendd))
                ic(v)
                results=srtsearch(appendd,v)
                print(results)
                global search_hwe_results
                search_hwe_results = results
                return redirect(reverse("search_results", kwargs={"srt_id": srt_id }))
            else:
                messages.success(request, "Please Enter atleast 1 keyword !!")
        else:
            messages.success(request,"Please Login to Use This Feature")
        
    return render(request,"newpreview.html",context)
def download_file2(request, driverFile):
    filename = driverFile
    filepath = os.path.join(settings.BASE_DIR,"media","srt_uploaded",driverFile)
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def search_results_view(request, srt_id):
    ic(search_hwe_results)
    obj=Srtgen.objects.get(id=srt_id)
    a=obj.file.url
    print(a , "ppp")
    aname=os.path.basename(a)
    f = open(obj.file.path,'r')
    srt_content = f.read()
    f.close()
    context={"obj":obj,"pathsrt":aname,"srt":srt_content, "search_results":search_hwe_results }
    if request.method=="POST":
        val=request.POST["key"]
        v=val.split(",")
        appendd=str(settings.BASE_DIR)+str(a)
        print(appendd,"hahha")
        results=srtsearch(appendd,v)
        print(results)
    return render(request,"searchResults.html",context)
def fav(request,srt_id):
    obj=Srtgen.objects.get(id=srt_id)
    Favourites.objects.create(user=request.user.authuser,link=obj)
    return redirect(reverse("history"))
def unfav(request, srt_id):
    obj=Srtgen.objects.get(id=srt_id)
    Favourites.objects.filter(user=request.user.authuser,link=obj).delete()
    return redirect(reverse("history"))
def downloadVideo(request, obj,start, end):
    theObject = Srtgen.objects.get(id=obj)
    clip = VideoFileClip(theObject.video.path)
    clip = clip.subclip(float(start), float(end))
    clip.write_videofile(f"{settings.BASE_DIR}/media/srt_uploaded/{theObject.title}.mp4")
    file_path = f"{settings.BASE_DIR}/media/srt_uploaded/{theObject.title}.mp4"
    filename = os.path.basename(file_path)
    mime = MimeTypes()
    url = pathname2url(file_path)
    mimetype, encoding = mime.guess_type(url)
    f = open(file_path, 'rb')
    response = HttpResponse(f.read(), content_type=mimetype)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = \
        "attachment; filename=\"%s\"; filename*=utf-8''%s" % \
        (filename, filename)
    f.close()
    return response
def show_srt(request, srt_id):
    obj=Srtgen.objects.get(id=srt_id)
    a=obj.file.url
    print(a , "ppp")
    aname=os.path.basename(a)
    f = open(obj.file.path,'r')
    srt_content = f.read()
    f.close()
    context={"obj":obj,"pathsrt":aname,"srt":srt_content }
    return render(request, "showSRT.html", context)