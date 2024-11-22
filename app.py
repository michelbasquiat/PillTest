from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

app = Flask(__name__)

# Function to draw wrapped text
def draw_text_box(draw, text, position, box_width, font, line_spacing=10, fill="black"):
    # Get the width of a single character
    char_width = font.getbbox('A')[2] - font.getbbox('A')[0]
    
    # Ensure char_width is valid
    if char_width <= 0:
        raise ValueError(f"Invalid character width calculated: {char_width}")
    
    # Ensure box_width is valid
    if box_width <= 0:
        raise ValueError(f"Invalid box width provided: {box_width}")
    
    # Calculate the maximum characters per line
    max_chars_per_line = box_width // char_width
    
    # Ensure max_chars_per_line is positive
    if max_chars_per_line <= 0:
        raise ValueError("Calculated maximum characters per line is invalid. Check box_width and font size.")
    
    # Wrap text
    lines = textwrap.wrap(text, width=max_chars_per_line)
    x, y = position
    for line in lines:
        line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height + line_spacing

# Function to generate the image
def generate_image(template_path, output_path, text_data, font_path="arial.ttf"):
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(font_path, size=85)
    for x, y, box_width, font_size, text in text_data:
        position = (x, y)
        font = ImageFont.truetype(font_path, size=font_size)
        draw_text_box(draw, text, position, box_width, font)
    template.save(output_path)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get user input
    responsavel = request.form.get('responsavel', '')
    registro_profissional = request.form.get('registro_profissional', '')
    projeto = request.form.get('projeto', '')
    proprietario = request.form.get('proprietario', '')
    endereco = request.form.get('endereco', '')
    criacao = request.form.get('criacao', '')
    projetista = request.form.get('projetista', '')
    conteudo = request.form.get('conteudo', '')
    escala = request.form.get('escala', '')
    data = request.form.get('data', '')
    prancha_n_1 = request.form.get('prancha_n_1', '')
    prancha_n_2 = request.form.get('prancha_n_2', '')

    # Define text data for the image
    text_data = [
        [255, 996, 1532, 85, projeto],
        [255, 1287, 1532, 85, proprietario],
        [255, 1582, 1532, 85, endereco],
        [1995, 996, 1532, 85, criacao],
        [1995, 1287, 1532, 85, projetista],
        [1995, 1582, 1532, 85, conteudo],
        [3736, 996, 649, 85, escala],
        [4598, 996, 649, 85, data],
        [3727, 286, 1532, 85, responsavel],
        [3727, 704, 1532, 85, registro_profissional],
        [4065, 1278, 800, 385, prancha_n_1],
        [4528, 1442, 800, 200, prancha_n_2],
    ]

    # Paths for the template and output
    template_path = "static/carimbo_template.png"
    output_path = "output.png"

    # Generate the image
    generate_image(template_path, output_path, text_data)

    # Serve the generated image
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False)
