import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lematools",                    
    version="0.0.1",                        
    author="LEMA-UFPB",                    
    description="LEMA-UFPB Tools",
    long_description=long_description,     
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',               
    py_modules=["lematools"],             
    #package_dir={'':''},     
    install_requires=['apache-airflow>=2.6']                    
)