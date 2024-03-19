import streamlit as st
from PIL import Image
from authtoken import authtoken

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

# Initialize Streamlit app
st.set_page_config(layout="wide")
st.title("Stable Diff Streamlit App")

# Create text input for prompt
prompt = st.text_area("Enter Prompt:", height=5)

# Load the model
model = "CompVis/stable-diffusion-v1-4"
pipeline = StableDiffusionPipeline.from_pretrained(model, revision="fp16", torch_dtype=torch.float16, use_auth_token=authtoken)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
pipeline.to(device)

# Function to generate image
def generate(prompt):
    with autocast(device):
        images = pipeline(prompt, guidance_scale=7).images
    
    image = images[0].to('cpu').detach().numpy()
    image = (image * 255).astype('uint8')
    return Image.fromarray(image)

# Generate button
if st.button("Generate"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            generated_image = generate(prompt)
        st.image(generated_image, use_column_width=True)

# Display model info
st.sidebar.title("Model Info")
st.sidebar.write("Model: CompVis/stable-diffusion-v1-4")
st.sidebar.write("Device:", device)
