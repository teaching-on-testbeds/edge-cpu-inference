import tflite_runtime.interpreter as tflite
from PIL import Image
import numpy as np

with open("labels.txt", 'r') as f:
    labels = [line.strip() for line in f.readlines()]

interpreter = tflite.Interpreter(model_path='mobilenet_v2_1.0_224_quantized_1_default_1.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

image_path = 'image.png'  
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
img = Image.open(image_path).resize((width, height))
img = img.convert('RGB')
input_data = np.array(img)
input_data = np.expand_dims(img, axis=0)

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])

sorted_result = sorted((e,i) for i,e in enumerate(output_data[0]))
top_3 = sorted_result[-3:][::-1]

for j,i in top_3:
  print('{:08.6f}: {}'.format(float(j / 255.0), labels[i].split(":")[1]))
