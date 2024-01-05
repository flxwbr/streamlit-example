import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import cv2
import zipfile

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.button('click me')

uploaded_files = st.file_uploader("Choose af file", accept_multiple_files=True)

if uploaded_files is not None:
    file_bytes = np.asarray(bytearray(uploaded_files[0].read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    st.image(opencv_image, caption='Image description')

    gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)

    st.image(gray_image, caption='Gray Image')

    Threshold = st.slider('Threshold', 0, 255, 127)

    _, binary_image = cv2.threshold(gray_image, Threshold, 255, cv2.THRESH_BINARY)

    st.image(binary_image, caption='Binary Image')

    height, width = binary_image.shape

    image_with_lines = binary_image.copy()

    images_vert = st.slider('Threshold', 0, 200, 10, key='vert')
    images_hor = st.slider('Threshold', 0, 200, 10, key='hor')

    piece_height = height // images_vert
    piece_width = width // images_hor    

    for i in range(1, images_vert):
        x = i * piece_width
        cv2.line(image_with_lines, (x, 0), (x, height), (0, 255, 0), 2)

    for j in range(1, images_hor):
        y = j * piece_height
        cv2.line(image_with_lines, (0, y), (width, y), (0, 255, 0), 2)

    st.image(image_with_lines,  caption='Precut Image')

    cut_images = []
    for row in range(images_vert):
        for col in range(images_hor):
            start_row = row * piece_height
            end_row = (row + 1) * piece_height
            start_col = col * piece_width
            end_col = (col + 1) * piece_width

            piece = binary_image[start_row:end_row, start_col:end_col]
            cut_images.append(piece)
    
    zip_filename = 'cut_images.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for i, piece in enumerate(cut_images):
            # Save each piece as a separate image
            piece_filename = f'piece_{i + 1}.png'
            cv2.imwrite(piece_filename, piece)

            # Add the saved image to the zip file
            zip_file.write(piece_filename)

            # Remove the temporarily saved image file
            os.remove(piece_filename)

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))
