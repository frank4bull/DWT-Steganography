import streamlit as st
from steganography import embed_message, extract_message

# Streamlit App
st.title("AI-Powered DWT Steganography")

# Sidebar for user input
st.sidebar.header("Options")
option = st.sidebar.selectbox("Choose Action", ["Embed Message", "Extract Message"])

if option == "Embed Message":
    st.header("Embed Message into Image")
    image_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
    message = st.text_input("Enter Secret Message")
    if image_file and message:
        with open("temp_image.png", "wb") as f:
            f.write(image_file.getbuffer())
        embed_message("temp_image.png", message, "stego_image.png")
        st.success("Message embedded successfully!")
        st.image("stego_image.png", caption="Stego Image", use_column_width=True)

elif option == "Extract Message":
    st.header("Extract Message from Image")
    stego_image_file = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"])
    if stego_image_file:
        with open("temp_stego_image.png", "wb") as f:
            f.write(stego_image_file.getbuffer())
        extracted_message = extract_message("temp_stego_image.png")
        st.success(f"Extracted Message: {extracted_message}")