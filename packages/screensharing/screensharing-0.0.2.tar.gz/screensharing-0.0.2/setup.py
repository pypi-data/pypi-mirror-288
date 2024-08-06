from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='screensharing',
    version='0.0.2',
    description='sharing your screen with other users in realtime',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Vishal Sharma, Raj kumar',
    author_email='vishalsharma659615@gmail.com, rky1524@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['screen-sharing', 'screen-casting', 'casting', 'display-sharing', 'realtime-screensharing',
              'realtime casting', 'video sharing'],
    packages=find_packages(),
    python_requires=">=3.7",
    Homepage="https://github.com/Vishal24102002/screenshare_lib",
    Issues="https://github.com/Vishal24102002/screenshare_lib/issues"
)
