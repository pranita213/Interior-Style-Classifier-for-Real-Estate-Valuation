import base64
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model


IMG_SHAPE = (224,224)
CLASSES = ["Modern", "Old"]
model = load_model('fine_tuned_house.keras')


app = Flask(__name__)

# basic first page
@app.route('/')
def sayhello():
      return render_template('index.html')

@app.route('/predict-interior', methods=['POST'])
def predict():
    f = request.files['img']
    fpath = getfpath(f)
    file = Image.open(f)
    file_shape = np.asarray(file).shape
# resize image to (224,224) if needed
    if file.size != IMG_SHAPE:
       file = file.resize(IMG_SHAPE)
       file_shape = np.asarray(file).shape
# predictions
    preds = model.predict(np.expand_dims(file, axis=0))[0]
    i = np.argmax(preds)
    label = CLASSES[i]
    prob = preds[i]
    
    pred_output={
      'img_size': file_shape,
      'label': label,
      'probability': np.round(prob*100,2)
      }
    return render_template('index.html',
                      img_shape=file_shape,
                      user_image=fpath,
                      pred_output=pred_output
                      )

def getfpath(img) -> str:
# convert to bases64
    data = img.read()              # get data from file (BytesIO)
    data = base64.b64encode(data)  # convert to base64 as bytes
    data = data.decode()           # convert bytes to string
    
    # convert to <img> with embed image
    fpath = "data:image/png;base64,{}".format(data)
    return fpath




if __name__=="__main__":
    app.run(debug=True)