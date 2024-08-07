from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()
setup(
    name="freeGPTFix",
    version="1.0.1",
    author_email="Redpiar.official@gmail.com",
    description="freeGPT provides free access to text and image generation models.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RedPiarOfficial/FreeGPTFix",
    author="RedPiar",
    license="MIT",
    keywords=[
        "artificial-intelligence",
        "machine-learning",
        "deep-learning",
        "gpt4free",
        "gpt4all",
        "freegpt",
        "chatgpt",
        "python",
        "llama",
        "llm",
        "nlp",
        "gpt",
        "ai",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],
    project_urls={
        "Source": "https://github.com/RedPiarOfficial/FreeGPTFix",
    },
)
