import setuptools

setuptools.setup(
    name="mcmod-resize",
    version="0.1.0",
    author="TunaFish2K",
    author_email="tunafish2k@163.com",
    description="auto-resize your item textures!",
    license="Apache-2.0",
    requires=["pillow"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": {
            "mcmod_resize=mcmod_resize:cli"
        }
    }
)