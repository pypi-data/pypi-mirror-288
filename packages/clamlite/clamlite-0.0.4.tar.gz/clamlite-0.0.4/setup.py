from setuptools import setup, find_packages

setup(
    name="clamlite",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        "timm>=0.9.8",
        "torch",
        "torchvision",
        "h5py",
        "pandas",
        "PyYAML",
        "opencv-python",
        "matplotlib",
        "scikit-learn",
        "scipy",
        "tqdm",
        "openslide-python",
        "tensorboardX"
    ],
)
