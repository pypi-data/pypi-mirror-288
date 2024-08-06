from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='phi-3-vision-mlx',
    url='https://github.com/JosefAlbers/Phi-3-Vision-MLX',
    py_modules=['phi_3_vision_mlx', 'gte', 'phi', 'api'],
    packages=find_packages(),
    version='0.1.5-beta',
    readme="README.md",
    author_email="albersj66@gmail.com",
    description="Phi-3-Vision on Apple silicon with MLX",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="MIT",
    python_requires=">=3.12.3",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "phi3v = phi_3_vision_mlx:chat_ui",
        ],
    },
    project_urls={
        "Documentation": "https://josefalbers.github.io/Phi-3-Vision-MLX/"
    },
)
