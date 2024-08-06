from setuptools import setup, find_packages

setup(
    name='uzbtelebot',
    version='0.0.8',
    packages=find_packages(),
    install_requires=[
        'telebot',  # telebot kutubxonasini o'rnatish uchun
    ],
    author='SalohiddinEsanbekov',
    author_email='salohiddinsalohiddin123@gmail.com',
    description='Agar siz telegram bot yasashni beginner darajasida bo\'lsangiz bu kutubxona siz uchun siz bu kutubxona orqali telegram bot yarata olasiz\n\nKutubxonani o\'rnatishpip install uzbtelebot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
