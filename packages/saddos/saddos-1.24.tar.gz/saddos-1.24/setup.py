from setuptools import setup, find_packages

setup(
    name='saddos',
    version='1.24',
    packages=find_packages(),
    install_requires=[
        # Daftar ketergantungan paket, jika ada-
    ],
    entry_points={
        'console_scripts': [
            'saddos=saddos.saddos:main',  # Ganti 'example' dan 'main' sesuai dengan nama modul dan fungsi utama Anda
        ],
    },
    python_requires='>=3.6',
    description='This Is Samp Exploit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fann',
    author_email='fancoding@outlook.com',
    url='https://github.com/RemonCalvius/saddos',  # Ganti dengan URL repositori Anda
)