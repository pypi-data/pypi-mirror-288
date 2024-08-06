import setuptools

setuptools.setup(
    name="mcmod-resize",
    packages=setuptools.find_packages(),
    author="TunaFish2K",
    description="resize your textures into mcmod.cn size!",
    version="0.1.1",
    install_requires=[
        "pillow"
    ],
    entry_points={
        "console_scripts": [
            "mcmod_resize=mcmod_resize:cli"
        ]
    }
)
