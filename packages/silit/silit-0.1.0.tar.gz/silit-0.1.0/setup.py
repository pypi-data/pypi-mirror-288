from setuptools import setup, find_packages

setup(
    name='silit',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'silit=silit.commands:create_project',
        ],
    },
    install_requires=[
        'flask',
    ],
    package_data={
        'silit': ['templates/project/**', 'templates/project/app/**', 'templates/project/public/**', 'templates/project/routes/**', 'templates/project/config/**'],
    },
    author='Nama Anda',
    author_email='email@anda.com',
    description='Framework untuk membuat aplikasi desktop dengan struktur MVC menggunakan Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/silit',  # Ganti dengan URL repositori Anda
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
