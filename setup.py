import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Django-CryptographicFields",
    version="2.0.1",
    author="Shahprogrammer",
    author_email="shahprogrammer05@gmail.com",
    description="A Django app for cryptography in Django Models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shahprogrammer/Django-CryptographicFields",
    packages=["CryptographicFields"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django :: 3.0",
        "Topic :: Security :: Cryptography",
        
    ],
    install_requires=[
          'django>=3.0.0','pycryptodome>=3.9.0',
      ],
    extras_require={
         ":python_version<'3.7'":["timestring"]
    },
    python_requires='>=3.6'
    )
