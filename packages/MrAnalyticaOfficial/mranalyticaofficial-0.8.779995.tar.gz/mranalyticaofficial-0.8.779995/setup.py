from setuptools import setup, find_packages

setup(
    name='MrAnalyticaOfficial',
    version='0.8.779995',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'tensorflow',  # Adicione tensorflow
        'scikit-learn'  # Adicione scikit-learn
    ],
    author='Matheus Rodrigo',
    author_email='mranalytica@mranalytica.com',
    description='Uma biblioteca poderosa para análise de dados, incluindo o módulo PhoenixVision para reconhecimento facial.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/user/MrAnalyticaOfficial',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)