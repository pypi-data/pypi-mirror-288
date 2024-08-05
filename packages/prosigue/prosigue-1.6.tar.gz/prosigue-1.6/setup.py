
from setuptools import setup

with open("readme.rst", "r", encoding="utf-8") as hoja:
    long_description = hoja.read()

setup(
        name= "prosigue",
        version= "1.6",
        author= "El Señor es el único eterno. Que la ciencia lo honre a Él.",
        author_email= "from.colombia.to.all@gmail.com",

        description= "Realiza una tarea secundaria en cierto tiempo dado. Pero si se cuelga, regresara aun asi al flujo de trabajo principal",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        
        license="Mozilla Public License 2.0 (MPL 2.0)",
        license_files=("license.txt",),
        
        packages= ["prosigue", "prosigue.standard", "prosigue.read_bookstores"],
        
        package_data={
            '': ['license.txt'],
        },
        include_package_data= True,
        url="https://github.com/Metal-Alcyone-zero/Prosigue",
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
        
        python_requires= ">=3.11.3"
        #install_requires=['multiprocessing', 'os', 'time'],
)

