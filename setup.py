import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Django-CryptographicFields", # Replace with your own username
    version="2.0.0",
    author="Shahprogrammer",
    author_email="shahprogrammer05@gmail.com",
    description="A Django app for cryptography in Django Models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shahprogrammer/Django-CryptographicFields",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django :: 3.0",
        "Topic :: Security :: Cryptography",
        
    ],
    install_requires=[
          'django>=3.0.0','pycryptodome>=3.9.0','timestring>=1.6.0'
      ],
  python_requires='>=3.6'
    )
