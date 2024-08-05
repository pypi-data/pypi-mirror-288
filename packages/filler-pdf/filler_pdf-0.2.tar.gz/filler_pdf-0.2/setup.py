from setuptools import setup, find_packages


with open("README.md","r") as f:
    description = f.read()

setup(
    name = "filler_pdf",
    version= '0.2',
    packages= find_packages(),
    author='Mayur Talreja',
    author_email='talrejamayur6@gmail.com',
    install_requires = [
        ## add dependencies
    ],

    # entry_points = {
    #     "console_scripts": [
    #         "pixegami-hello = pixegami_hello:hello",

    #     ],
    # },

    long_description=description,
    long_description_content_type="text/markdown",
)