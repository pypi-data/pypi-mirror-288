from setuptools import setup, find_packages

setup(
    name="terrenos",
    version="4.0.0",
    packages=find_packages(),
    author="dvanegasf",
    author_email="tu_email@example.com",
    description="Paquete para trabajar con capas de terrenos y validar atributos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/tu_repositorio",  # URL de tu repositorio
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)