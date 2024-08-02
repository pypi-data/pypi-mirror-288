# Certificate Generator

A Python package to generate certificates with a given name and a logo in the top middle.

## Features

- Generate certificates with a specified template.
- Add a custom logo to the top middle of the certificate.
- Customize the font and color of the text.
- Save generated certificates as PNG files.

## Installation

You can install the package from PyPI using pip:

```bash
pip install certificate_generator
```

## Usage

### Basic Usage

To generate certificates, you need a template image, a font file, and a logo image. Here's an example of how to use the package:

```python
from certificate_generator import CertificateGenerator

template_path = 'path/to/template.png'
font_path = 'path/to/font/GreatVibes-Regular.ttf'
logo_path = 'path/to/logo.png'

generator = CertificateGenerator(template_path, font_path, logo_path)

# Example names
names = ["Alice", "Bob", "Charlie"]

for name in names:
    generator.create_certificate(name)
```

### Command Line Usage

You can also generate certificates using the command line. Make sure you have a `names.txt` file with each name on a new line:

```bash
generate-certificates
```

### Customization

You can customize the font size and color when creating the `CertificateGenerator` instance:

```python
generator = CertificateGenerator(template_path, font_path, logo_path, font_size=150, font_color="#000000")
```


### Output Directory

By default, the certificates are saved in an `out` directory. You can specify a different output directory:

```python
generator.create_certificate(name, output_dir="./custom_output/")
```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Tushar Nankani](https://github.com/tusharnankani/) - Main author of the basic script

[Asib Hossen](https://github.com/asibhossen897)

## Acknowledgements

- [Pillow](https://python-pillow.org/) - The friendly PIL fork.
