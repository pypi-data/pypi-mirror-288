# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="physicsLab",
    version="1.4.11",
    license="MIT",
    author="Goodenough",
    author_email="2381642961@qq.com",
    description="Python API for Physics-Lab-AR",
    long_description="click \"[there](https://gitee.com/script2000/physicsLab)\" or "
                     "[there](https://github.com/GoodenoughPhysicsLab/physicsLab) to show more information",
    long_description_content_type="text/markdown",
    url="https://gitee.com/script2000/physicsLab",
    packages=setuptools.find_packages(),
    install_requires=["mido", "typing-extensions", "requests", "colorama"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
