# Importing necessary modules
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import SparseCategoricalCrossentropy

# Load the saved model without compilation
model = load_model('road_violation_model3.keras', compile=False)

# Recompile the model with the correct loss function
model.compile(
    loss=SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)

# Load class names from a CSV file
classes = pd.read_csv('labels.csv')

# Initializing the main window
root = tk.Tk()
root.geometry('900x600')
root.title('🚦 Traffic Sign Detection 🚦')
root.configure(background='#E0F7FA')

# ------------------------- Frames for UI Components -------------------------

# Header Section
header_frame = tk.Frame(root, bg='#283747', height=80)
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="🚦 Traffic Sign Detection",
                         font=('Arial', 24, 'bold'), bg='#283747', fg='white')
header_label.pack(pady=20)

# Sidebar for Buttons (Upload and Classify)
sidebar_frame = tk.Frame(root, width=200, bg='#283747')
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

btn_upload = tk.Button(sidebar_frame, text="Upload Image", font=('Arial', 15),
                       bg='#2E86C1', command=lambda: upload_image())
btn_upload.pack(pady=20, fill=tk.X, padx=20)

btn_classify = tk.Button(sidebar_frame, text="Classify Image", font=('Arial', 15),
                         bg='#2E86C1', command=lambda: classify(uploaded_file_path))
btn_classify.pack(pady=20, fill=tk.X, padx=20)

# Main display area for the uploaded image and predictions
main_display = tk.Frame(root, bg='white')
main_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

label_predictions = tk.Label(main_display, text='', font=('Arial', 18),
                             bg='white', anchor=tk.W, justify=tk.LEFT)

label_predictions.pack(fill=tk.X, padx=10, pady=10)

sign_display = tk.Label(main_display)

sign_display.pack(expand=True)

uploaded_file_path = None  # To store the path of the uploaded image

# Function to classify the uploaded image
def classify(file_path):
    if file_path:
        image = Image.open(file_path).convert('RGB')
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        predictions = model.predict(image)[0]
        threshold = 0.05
        detected_signs = [(classes['Name'][i], prob) for i, prob in enumerate(predictions) if prob > threshold]

        if detected_signs:
            result_text = "\n".join([f"{name}: {prob:.2f}" for name, prob in detected_signs])
        else:
            result_text = "No signs detected with confidence > 0.05"

        label_predictions.configure(text=f"Predictions:\n{result_text}")

# Function to upload an image
def upload_image():
    global uploaded_file_path
    uploaded_file_path = filedialog.askopenfilename()

    if uploaded_file_path:
        uploaded_img = Image.open(uploaded_file_path)
        uploaded_img.thumbnail((600, 400))

        img_display = ImageTk.PhotoImage(uploaded_img)
        sign_display.configure(image=img_display)
        sign_display.image = img_display

        label_predictions.configure(text='')

# Start the main window loop
root.mainloop()
