from setuptools import setup, find_packages

setup(
    name="vkmusix",
    version="0.1.0",
    description="Библиотека для взаимодействия в VK Music. Документация: vkmusix.ru/docs.",
    long_description=open('README.md').read(),  # Чтение описания из файла README.md
    long_description_content_type='text/markdown',  # Указание формата README.md
    author="thswq",
    author_email="admin@vkmusix.ru",
    url="https://github.com/to4no4sv/vkmusix",
    packages=find_packages(),
    install_requires=[
        "pytz == 2022.1",
        "httpx == 0.27.0",
        "aiofiles == 23.2.1",
        "selenium == 4.21.0",
        "webdriver_manager == 4.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)