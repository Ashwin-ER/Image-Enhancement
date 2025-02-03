# Based on https://huggingface.co/spaces/keras-io/Enhance_Low_Light_Image
import streamlit as st
import os
from datetime import datetime
from PIL import Image, ImageOps
from io import BytesIO

from src.st_style import apply_prod_style

apply_prod_style(st)  # NOTE: Uncomment this for production!

def image_download_button(pil_image, filename: str, fmt: str, label="Download"):
    if fmt not in ["jpg", "png"]:
        raise Exception(f"Unknown image format (Available: {fmt} - case sensitive)")
    
    pil_format = "JPEG" if fmt == "jpg" else "PNG"
    file_format = "jpg" if fmt == "jpg" else "png"
    mime = "image/jpeg" if fmt == "jpg" else "image/png"
    
    buf = BytesIO()
    pil_image.save(buf, format=pil_format)
    
    return st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=f'{filename}.{file_format}',
        mime=mime,
    )

st.title("Enhance Low Light Image using Zero-DCE")
st.image(Image.open("photo-low-light-enhance/assets/demo.jpg"))  # Updated path

uploaded_file = st.file_uploader(
    label="Upload your photo here", 
    accept_multiple_files=False, 
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    with st.expander("Original photo", expanded=True):
        if uploaded_file is not None:
            st.image(uploaded_file)
        else:
            st.warning("You haven't uploaded any photo yet")

    if st.button("Enhance") and uploaded_file is not None:
        img_input = Image.open(uploaded_file).convert("RGB")
        
        with st.spinner("AI is doing the magic"):
            img_output = ImageOps.autocontrast(img_input, 3)
        
        with st.expander("Success!", expanded=True):
            st.image(img_output)
            uploaded_name = os.path.splitext(uploaded_file.name)[0]
            image_download_button(
                pil_image=img_output,
                filename=uploaded_name,
                fmt="jpg",
                label="Download Image",
            )
