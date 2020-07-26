import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='kindle_bot',  
    version='0.1',
    scripts=[] ,
    author="Antonino Elia Mandri, Andrea Finazzi",
    author_email="deepak.kumar.iet@gmail.com",
    description="Convert html pages to pdf and send to kindle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antoninoelia/kindle_bot",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )