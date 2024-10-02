from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os
import random
from transformers import CLIPProcessor, CLIPModel
import torch
from train_model import fine_tune_model
from video_generator import generate_video_from_banner

app = Flask(__name__)

# Traditional banner generation logic
def generate_banner(product_image_path, promo_text, theme, color_palette):
    try:
        product_image = Image.open(product_image_path).convert("RGBA")
        banner = Image.new('RGBA', (1360, 800), random.choice(color_palette))
        banner.paste(product_image, (100, 100), product_image)

        # Draw promotional text
        draw = ImageDraw.Draw(banner)
        font = ImageFont.truetype("arial.ttf", 50)
        draw.text((150, 700), promo_text, fill="white", font=font)

        # Apply theme decorations (e.g., Diwali lights, flags for Independence Day)
        if theme == "Diwali":
            diwali_overlay = Image.open("static/diwali_overlay.png").convert("RGBA")
            banner.paste(diwali_overlay, (0, 0), diwali_overlay)

        output_path = "static/output/banner_output.png"
        banner.save(output_path)
        return output_path
    except Exception as e:
        print(e)
        return None

# AI-powered banner generation logic using CLIP
def generate_banner_with_ai(product_image_path, promo_text):
    try:
        model = CLIPModel.from_pretrained("models/fine_tuned")  # Use fine-tuned model if available
        processor = CLIPProcessor.from_pretrained("models/fine_tuned")

        product_image = Image.open(product_image_path).convert("RGBA")
        inputs = processor(text=promo_text, images=product_image, return_tensors="pt", padding=True)

        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        similarity_score = logits_per_image.item()

        # AI-determined layout and color
        banner = Image.new('RGBA', (1360, 800), (255, 223, 186))
        banner.paste(product_image, (int(similarity_score * 500), 100), product_image)

        # Draw promotional text
        draw = ImageDraw.Draw(banner)
        font = ImageFont.truetype("arial.ttf", 50)
        draw.text((int(similarity_score * 300), 700), promo_text, fill="white", font=font)

        output_path = "static/output/banner_output_ai.png"
        banner.save(output_path)
        return output_path
    except Exception as e:
        print(e)
        return None

# Route for generating banners (with or without AI)
@app.route('/generate_banner', methods=['POST'])
def generate_banner_route():
    try:
        image = request.files['image']
        promo_text = request.form['promoText']
        theme = request.form['theme']
        use_ai = request.form.get('useAI', 'false') == 'true'

        image_path = os.path.join('static/uploads', image.filename)
        image.save(image_path)

        color_palette = [(255, 228, 196), (255, 235, 205), (255, 223, 186)]

        if use_ai:
            banner_path = generate_banner_with_ai(image_path, promo_text)
        else:
            banner_path = generate_banner(image_path, promo_text, theme, color_palette)

        if banner_path:
            return jsonify({"message": "Banner generated", "banner_url": banner_path})
        else:
            return jsonify({"error": "Banner generation failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for video generation
@app.route('/generate_video', methods=['POST'])
def generate_video_route():
    try:
        image = request.files['image']
        promo_text = request.form['promoText']
        theme = request.form['theme']
        use_ai = request.form.get('useAI', 'false') == 'true'

        image_path = os.path.join('static/uploads', image.filename)
        image.save(image_path)

        color_palette = [(255, 228, 196), (255, 235, 205), (255, 223, 186)]

        if use_ai:
            banner_path = generate_banner_with_ai(image_path, promo_text)
        else:
            banner_path = generate_banner(image_path, promo_text, theme, color_palette)

        # Generate video from the banner
        video_output_path = "static/output"
        video_path = generate_video_from_banner(banner_path, promo_text, video_output_path)

        if video_path:
            return jsonify({"message": "Video generated", "video_url": video_path})
        else:
            return jsonify({"error": "Video generation failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for model fine-tuning
@app.route('/train_model', methods=['POST'])
def train_model_route():
    try:
        images = request.files.getlist('images')
        texts = request.form.getlist('texts')

        image_paths = []
        for image in images:
            image_path = os.path.join('static/uploads', image.filename)
            image.save(image_path)
            image_paths.append(image_path)

        fine_tune_model(image_paths, texts)

        return jsonify({"message": "Model fine-tuned successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    if not os.path.exists('static/output'):
        os.makedirs('static/output')
    if not os.path.exists('models/fine_tuned'):
        os.makedirs('models/fine_tuned')
    app.run(debug=True, host='0.0.0.0', port=5000)
