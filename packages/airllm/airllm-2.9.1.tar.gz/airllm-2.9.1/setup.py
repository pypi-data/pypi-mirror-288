import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airllm",
    version="2.9.1",
    author="Gavin Li",
    author_email="gavinli@animaai.cloud",
    description="AirLLM allows single 4GB GPU card to run 70B large language models without quantization, distillation or pruning. 8GB vmem to run 405B Llama3.1.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lyogavin/airllm",
    packages=setuptools.find_packages(),
    install_requires=[
        'tqdm',
        'torch',
        'transformers',
        'accelerate',
        'safetensors',
        'optimum',
        'huggingface-hub',
        'scipy',
        #'bitsandbytes' set it to optional to support fallback when not installable
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
