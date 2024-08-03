from setuptools import setup, find_packages
import pathlib

# Получить путь к текущему каталогу
here = pathlib.Path(__file__).parent.resolve()

# Прочитать содержимое README.md
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='kandinskylib',  # Имя вашего пакета
    version='0.1.3',  # Обновите версию здесь
    description='A library for working with Kandinsky AI image generator API',  # Краткое описание
    long_description=long_description,  # Длинное описание из README.md
    long_description_content_type='text/markdown',  # Тип содержимого длинного описания
    url='https://github.com/Read1dno/kandinskylib',  # URL вашего проекта
    author='Read1dno',
    author_email='ef8ser@gmail.com',
    classifiers=[  # Классификаторы для PyPI
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='kandinsky, ai, image generation, api',  # Ключевые слова
    packages=find_packages(),  # Автоматический поиск пакетов
    python_requires='>=3.6, <4',
    install_requires=['requests', 'pillow'],  # Зависимости
)
