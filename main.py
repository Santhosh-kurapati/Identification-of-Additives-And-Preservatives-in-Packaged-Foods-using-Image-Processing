from flask import Flask, render_template, request
import os, io
from google.cloud import vision
import pandas as pd
import cv2
import re
from werkzeug.utils import secure_filename
app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

import google.generativeai as gai
ak="AIzaSyAbOUYpgtvdsLFYVSDZrFKv5jx7zwOBSws"
gai.configure(api_key=ak)

m=gai.GenerativeModel("gemini-1.0-pro-vision-latest")
p='extract text from image'
r=m.generate_content([p,i])
print(r.text)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods = ['POST'])
def getvalue():
  name = request.form['sname']
  if name:
   z=[name]
   arr=search(z)
   return render_template("index.html", arr=arr, l=len(arr))
  else:
   file = request.files['file']
   filename = secure_filename(file.filename)
   file.save(os.path.join(app.config['UPLOAD'], filename))
   img = os.path.join(app.config['UPLOAD'], filename)
   im = cv2.imread(img)
   z=google(file.filename)
   arr=search(z)
   return render_template("index.html", arr=arr, l=len(arr),img=img)

def search(z):
  df = pd.read_excel('C:\Users\Lenovo\Desktop\Main project\dataset-main project.xlsx')
  ans=[]
  Data = {}
  for i, r in df.iterrows():
   Data[r[0]] = [r[1], r[2]]
  k=1
  for e in z:
   if e in Data:
    ans.append([k,e,Data[e][0],Data[e][1]])
    k+=1
  return ans

def google(File_Name):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\sekha\PycharmProjects\pythonProject\venv\projectkey.json"
 # create client instance
    client = vision.ImageAnnotatorClient()
    Folder_Path = r"C:\Users\sekha\PycharmProjects\pythonProject\static\uploads"

    with io.open(os.path.join(Folder_Path, File_Name), 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    ans = ""
     for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
     # print('Paragraph confidence: {}'.format(
     # paragraph.confidence))
                s = ""
                for word in paragraph.words:
                    word_text = ''.join([ symbol.text for symbol in word.symbols ])
                    s += word_text
                ans = ans + " " + s
     # print(s)
     # using regex module to filter the raw string
     ad = re.findall(r"\bINS\w+", ans)
     return ad

if __name__ == "__main__":
 app.run()