import sys
import tkinter as tk
import customtkinter as ctk

from PIL import ImageTk
from authtoken import authtoken

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


app =  tk.Tk()
app.geometry("532x622")
app.title("Stable Diff")
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

prompt = ctk.CTkEntry(app, height=40, width=512, font = ("Arial", 20), text_color="black", fg_color="white")
prompt.place(x=10, y=10)

lmain = ctk.CTkLabel(app, height=512, width=512, fg_color="transparent", text = "")
lmain.configure()
lmain.place(x=10, y=110)

model = "CompVis/stable-diffusion-v1-4"
pipeline = StableDiffusionPipeline.from_pretrained(model, revision = "fp16", torch_dtype = torch.float16, use_auth_token = authtoken)
device = 'cuda'
pipeline.to(device)

def generate():
    with autocast(device):
        images = pipeline(prompt.get(), guidance_scale = 7).images
    
    image = images[0]
    image.save('generateimage.png')
    img = ImageTk.PhotoImage(image)
    lmain.configure(image = img)

trigger = ctk.CTkButton(app, height=40, width=120, font = ("Arial", 20), text_color="white", fg_color="Red", command=generate)
trigger.configure(text = "Generate")
trigger.place(x=206, y=60)

app.mainloop()