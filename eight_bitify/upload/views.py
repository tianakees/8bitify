from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image

def next(a,b,c,d,size,box_size):
    if(c != size):
        return a+box_size, b, c+box_size, d
    else:
        return 0, b+box_size, box_size, d+box_size

def handle_uploaded_file(f):
    im = Image.open(f)
    size = im.width
    box_size = 4    
    ht = im.height
    im = im.resize((size-224, ht-96)) #TODO reduce the size proportionately
    im = im.convert('P',colors=8)
    left, top, right, bottom = 0, 0, box_size, box_size

    while(not(top == size)):
        box = (left, top, right, bottom)
        region = im.crop(box)
        # fill = sorted(region.getcolors(), reverse=True)[0][1]
        fill = list(region.getcolors())[0][1]
        im.paste(fill, box)
        left,top,right,bottom = next(left, top, right, bottom, size, box_size)

    im = im.convert('RGB')
    return im

def test_uploaded_file(f):
    im = Image.open(f)
    # src = Image.open('8col.png')
    # im = im.quantize(palette = src)

    size = im.width
    box_size = 4    
    ht = im.height
    im = im.resize((size-224, ht-96)) #TODO reduce the size proportionately

    im = im.convert('P')
    left, top, right, bottom = 0, 0, box_size, box_size

    while(not(top == size)):
        box = (left, top, right, bottom)
        region = im.crop(box)
        fill = sorted(region.getcolors(), reverse=True)[0][1]
        
        im.paste(fill, box)
        left,top,right,bottom = next(left, top, right, bottom, size, box_size)

    im = im.convert('RGB')
    return im

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            processed_image = test_uploaded_file(request.FILES['image'])

            #img = Image.open(processed_image)
            response = HttpResponse(content_type="image/png")
            processed_image.save(response, "PNG")
            return response

            #return render(request, 'bye.html', {'image': processed_image})
            #return HttpResponseRedirect('bye/', kwargs={'p_image': processed_image})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def bye(request, p_image):
    return render(request, 'bye.html', {'image': p_image})
