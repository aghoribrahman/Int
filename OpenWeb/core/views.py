from django.shortcuts import render
import os
from PyPDF2 import PdfReader, PdfFileReader
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from core.forms import FolderUploadForm
from core.models import PDFFile
from gtts import gTTS

def index(request):
    return render(request,'index.html')

def upload_folder(request):
    if request.method == 'POST':
        form = FolderUploadForm(request.POST, request.FILES)
        if form.is_valid():
            folder = request.FILES.getlist('folder')
            fs = FileSystemStorage()

            for pdf_file in folder:
                # Save the PDF file to a temporary location
                fs.save(pdf_file.name, pdf_file)
                pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)

                # Extract text from PDF
                with open(pdf_path, 'rb') as file:
                    pdf = PdfReader(file)
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text()

                # Create a text file and save the extracted text
                txt_file_name = os.path.splitext(pdf_file.name)[0] + '.txt'
                txt_file_path = os.path.join(settings.MEDIA_ROOT, txt_file_name)
                with open(txt_file_path, 'w', encoding='utf-8') as file:
                    file.write(text)

                # Delete the temporary PDF file
                fs.delete(pdf_file.name)

            return render(request, 'upload.html')
    else:
        form = FolderUploadForm()
    return render(request, 'upload.html', {'form': form})

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        
        
        save_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
        text = extract_text_from_pdf(pdf_file)
        with open(save_path, 'wb') as file:
            for chunk in pdf_file.chunks():
                file.write(chunk)
                
        context = {'text': text}
        return render(request,'index.html',context)  # Redirect to a success page after upload

    return render(request, 'index.html')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
      
    return text

def text_to_audio(paragraphs):
    for i, paragraph in enumerate(paragraphs):
        tts = gTTS(text=paragraph, lang='en')
        filename = f"output_{i}.mp3"
        file_path = os.path.join('media', filename)
        print(file_path)

        tts.save(file_path)

def extract_text_from_directory(request):
    directory_path = '/path/to/directory'  # Replace with the actual directory path
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, file_name)
            text = extract_text_from_pdf(pdf_path)

            # Save extracted text to a text file
            text_file_path = os.path.splitext(pdf_path)[0] + '.txt'
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            print(f"Extracted text from {pdf_path} and saved to {text_file_path}")
          

    return HttpResponse("Text extraction completed.")



