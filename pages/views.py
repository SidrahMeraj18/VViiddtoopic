from glob import glob
from django.shortcuts import redirect, render
from srtgen.models import Srtgen
from wh import createSearchableData
# Create your views here.
from icecream import ic
hitObjs = []
def home(request):
    objs = Srtgen.objects.filter(public=True)
    ic(objs)
    if request.method == "POST":
        keyword = request.POST["search"]
        ic(keyword)
        # pleaseSearchTheSRTs(keyword)
        return redirect("search_result", keyword=keyword)
    return render(request, 'newhome.html', {"home":True, "objs":objs})
def search_result(request, keyword):
    global hitObjs
    hitObjs = []
    objs = Srtgen.objects.filter(public=True)
    for obj in objs:
        if obj.file:
            ic(obj.file.path)
            result = createSearchableData(obj.file.path, keyword)
            ic(result)
            if result != False:
                hitObjs.append(obj)
    if request.method == "POST":
        keyword = request.POST["search"]
        ic(keyword)
        return redirect("search_result", keyword=keyword)
    return render(request, "search_result.html", {"objs":hitObjs, "keyword":keyword})