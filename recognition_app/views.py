from django.shortcuts import render
from pyscreeze import locate
from .models import gujrati_files
from PIL import Image
import pytesseract
import os
from pdf2image import convert_from_path


# ,poppler_path=r'C:\Program Files\poppler-22.04.0\Library\bin'


def scanhompage(request):
    return render(request,'scan.html')

def check_endwith(child_dir):
    end = 1
    c_dir = child_dir + f'_{end}'
    end=end+1
    if(os.path.exists(c_dir)):
                c_dir = check_endwith(c_dir)
    return c_dir
    
def check_pdf_path(filename,filename2):
    if(os.path.exists('Uploaded_Data/pdf/')):
            
            child_dir = 'Uploaded_Data/pdf/'+f'{filename}'
            if(os.path.exists(child_dir)):
                child_dir = check_endwith(child_dir)
            os.mkdir(child_dir)
            tex = pdf_to_image(filename2,child_dir)
            return tex
           
    else:
            parent = 'Uploaded_Data'
            p_dir = 'pdf'
            pdf_dir = os.path.join(parent,p_dir)
            child_dir = pdf_dir+"/" + f'{filename}'
            os.mkdir(pdf_dir)
            os.mkdir(child_dir)

            tex = pdf_to_image(filename2,child_dir)
            return tex


def pdf_to_image(location,child_dir):
        tex = ""
        images = convert_from_path(f'Uploaded_Data/{location}',500)
        for i in range(len(images)):
                f_name = child_dir+'/page'+ str(i) +'.jpg'
                images[i].save(f_name)
                tex = tex + pdf_data(f_name)
        return tex
            
            

def pdf_data(filename):
    # for i in os.listdir(child_dir):
    tex= pytesseract.image_to_string(Image.open(f'{filename}'),lang='guj')
    return tex


def save_file(filename,extension,tex):
    locate = ''
    if(extension == 'pdf'):
            with open(f'result/pdf/{filename}.doc', 'w', encoding='utf-8') as f:
                f.write(tex)
                locate = f'pdf/{filename}.doc'
    else:
             with open(f'result/img/{filename}.doc', 'w', encoding='utf-8') as f:
                f.write(tex)
                locate = f'img/{filename}.doc'
    return locate


def recogntion(request):
    text_frontend = {}
    image = request.FILES['image']
    data = gujrati_files()
    data.image = image
    data.save()
    
    filename = str(image)
    filename2 = str(image)
    filename = filename.split(".")
    extension = filename[1]
    filename = filename[0]
    
    tex = ''
    
    
    
    if(extension == 'pdf'):
        tex = tex + check_pdf_path(filename,filename2)
                    
    else:
    
        tex= tex + pytesseract.image_to_string(Image.open(f'Uploaded_Data/{filename2}'),lang='guj')
    
    
    if(os.path.exists('result/pdf')):
        location = save_file(filename,extension,tex)
    
            
    else:
        parent='result/'
        i_dir = 'img'
        p_dir = 'pdf'
        img_dir = os.path.join(parent,i_dir)
        pdf_dir = os.path.join(parent,p_dir)
        os.mkdir('result')
        os.mkdir(img_dir)
        os.mkdir(pdf_dir)
        location = save_file(filename,extension,tex)
        
    text_frontend.update({'text':tex,
                          'location':location})
    return render(request,'result.html',text_frontend)
    