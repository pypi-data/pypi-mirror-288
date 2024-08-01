from setuptools import setup, find_packages
import os

# Definicja funkcji, która uruchomi skrypt post-instalacyjny
def post_install():
    os.system('python post_install.py')

setup(
    name='mwalas_skk_hello',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Zależności pakietu
    ],
    entry_points={
        'console_scripts': [
            'my_package_mwalas_skk=my_package_mwalas_skk.hello:main',  # Zdefiniuj funkcję main w hello.py
        ],
    },
)

print("\nPakiet został zainstalowany. Proszę uruchomić skrypt post_install.py, aby dokończyć instalację.")