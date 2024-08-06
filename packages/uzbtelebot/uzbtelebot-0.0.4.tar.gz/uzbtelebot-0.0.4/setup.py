from setuptools import setup, find_packages

setup(
    name='uzbtelebot',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'telebot',  # telebot kutubxonasini o'rnatish uchun
    ],
    author='SalohiddinEsanbekov',
    author_email='salohiddinsalohiddin123@gmail.com',
    description='siz bu bot orqali telegram bot yarata olasiz',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
