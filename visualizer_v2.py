from PIL import Image, ImageDraw, ImageTk
from colors import label2color
import json
import tkinter as tk

filename = 'resume_1_0'

annotations_dir = '../done'
images_dir = '../annotations_images_louise'

with open(f'{annotations_dir}/{filename}.json', 'r', encoding='utf-8') as file:
    cache = json.load(file)

first_run = True

def update_image(cache: dict):
    global img, draw, canvas, image_item, first_run

    # Reload the JSON data
    with open(f'{annotations_dir}/{filename}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data != cache or first_run:
        if first_run:
            first_run = False

        cache = data

        # Load the image
        img = Image.open(f'{images_dir}/{filename}.jpeg')
        draw = ImageDraw.Draw(img)

        for entry in data['form']:
            # The following code visualizes the bounding boxes of a single entry
            box = entry['box']
            label = entry['label']  # Get the label name
            draw.rectangle(box, outline=label2color[label], width=2)
            if label:
                # Display the label name near the bounding box
                draw.text((box[0], box[1] - 10), label, fill=label2color[label])

        # Update the canvas with the new image and adjust the window size
        width, height = img.size
        canvas.config(width=width, height=height)
        photo = ImageTk.PhotoImage(img)
        canvas.itemconfig(image_item, image=photo)
        canvas.image = photo

    # Schedule the next update in 1 second (adjust as needed)
    root.after(1000, update_image, cache)

# Create the main application window
root = tk.Tk()
root.title("Real-time Bounding Box Viewer")

# Create a Canvas to display the image
canvas = tk.Canvas(root)
canvas.pack()

# Load and display the image initially
img = Image.open(f'{images_dir}/{filename}.jpeg')
photo = ImageTk.PhotoImage(img)
image_item = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Update the image
update_image(cache)

# Start the main loop
root.mainloop()
