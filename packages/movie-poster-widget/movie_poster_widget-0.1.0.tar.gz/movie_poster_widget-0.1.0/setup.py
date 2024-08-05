from setuptools import setup, find_packages

setup(
    name="movie_poster_widget",
    version="0.1.0",
    description="A widget for displaying movie posters",
    author="Votre Nom",
    author_email="votre.email@example.com",
    url="https://github.com/votre_nom/movie_poster_widget",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PySide6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
