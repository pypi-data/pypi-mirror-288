import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as fh:
    license_content = fh.read()

setuptools.setup(
    name="medusa-vision",
    version="0.2.1",
    author="vortezwohl",
    author_email="2310108909@qq.com",
    description="Emotion and gender recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vortezwohl/medusa-vision",
    project_urls={
        "Bug Tracker": "https://github.com/vortezwohl/medusa-vision/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=[
        'opencv-python==4.10.0.84',
        'keras==3.4.1',
        'numpy==1.26.4',
        'tensorflow==2.16.2'
    ],
    license=license_content
)
