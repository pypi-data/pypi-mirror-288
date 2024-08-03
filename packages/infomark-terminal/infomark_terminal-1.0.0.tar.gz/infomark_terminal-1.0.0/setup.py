from setuptools import setup, find_packages

setup(
    name="infomark-terminal",  # Name of your package
    version="1.0.0",  # Version of your package
    author="CK127",  # Replace with your name
    author_email="kcelestinomaria127@gmail.com",  # Your email
    description="Infomark Terminal: A Financial Markets Data terminal for educational use",
    long_description=open('README.md').read(),  # Assumes you have a README file
    long_description_content_type="text/markdown",
    url="https://github.com/kcelestinomaria/infomark-terminal",  # Replace with your project URL
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust based on your requirements
    install_requires=[
        "requests",
        "pandas",
        "numpy",
        "matplotlib",
        "plotly",
        "dash",
        "streamlit",
        "scikit-learn",
        "sqlalchemy",
        # Add other dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'infomark-terminal=infomark_terminal.__main__:main',  # Update this if the entry point is different
        ],
    },
)
