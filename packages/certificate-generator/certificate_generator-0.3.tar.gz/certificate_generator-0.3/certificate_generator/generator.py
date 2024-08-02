# certificates/certificate_generator/generator.py

from PIL import Image, ImageFont, ImageDraw
import os


class CertificateGenerator:
    def __init__(self, template_path, font_path, logo_path, font_size=180, font_color="#FFFFFF"):
        self.template_path = template_path
        self.font_path = font_path
        self.logo_path = logo_path
        self.font_size = font_size
        self.font_color = font_color

        self.template = Image.open(self.template_path)
        self.width, self.height = self.template.size
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def add_logo(self, image_source):
        logo = Image.open(self.logo_path)
        logo_width, logo_height = logo.size

        # Center the logo horizontally and position it near the top
        logo_position = ((self.width - logo_width) // 2, (self.height - logo_height) // 12)
        image_source.paste(logo, logo_position, logo)
        return image_source

    def add_text(self, image_source, name):
        draw = ImageDraw.Draw(image_source)

        # Finding the bounding box of the text.
        bbox = draw.textbbox((0, 0), name, font=self.font)
        name_width = bbox[2] - bbox[0]
        name_height = bbox[3] - bbox[1]

        # Placing it in the center, then making some adjustments.
        draw.text(((self.width - name_width) / 2, (self.height - name_height) / 2 - 30), name, fill=self.font_color,
                  font=self.font)

    def create_certificate(self, name, output_dir="./out/"):
        '''Function to save certificates as a .png file'''

        image_source = self.template.copy()
        image_source = self.add_logo(image_source)
        self.add_text(image_source, name)

        # Saving the certificates in a different directory.
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{name}.png")
        image_source.save(output_path)
        print('Saving Certificate of:', name)
        print()


def main():
    template_path = os.path.join(os.path.dirname(__file__), 'template.png')
    font_path = os.path.join(os.path.dirname(__file__), 'font', 'GreatVibes-Regular.ttf')
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')

    generator = CertificateGenerator(template_path, font_path, logo_path)

    names = []
    with open('names.txt', 'r') as f:
        names = f.read().splitlines()

    for name in names:
        generator.create_certificate(name)
    print(len(names), "certificates done.")


if __name__ == "__main__":
    main()
