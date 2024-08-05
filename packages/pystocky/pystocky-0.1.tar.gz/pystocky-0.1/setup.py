from setuptools import setup, find_packages

setup(
    nanme='pystocky',
    version='0.1',
    packages=find_packages(),
    description='A PyTorch based stock model training and prediction library',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/dtsroy/stock-prediction',
    author='dtsroy',
    author_email='dtsroy39@gmail.com',
    license='GNU General Public License v3',
    python_requires='>=3.6',
    install_requires=[
        'torch',
        'swanlab',
        'pandas',
        'scikit-learn',
        'numpy',
        'tqdm',
        'matplotlib'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ]
)
