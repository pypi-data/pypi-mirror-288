from setuptools import setup, find_packages


def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        return f.read()


attrs = dict(
    name='face_detector_plus',
    version="0.1.0",
    packages=find_packages(exclude=('test',)),
    long_description=get_long_description('README.md'),
    description='Light weight face detector high-level client with multiple detection techniques.',
    long_description_content_type='text/markdown',
    author="Huseyin Das",
    author_email='hsyndass@gmail.com',
    url='https://github.com/huseyindas/face-detectors',
    license='Apache',
    python_requires='>=3.9',
    setup_requires=[
        "cmake==3.21.1.post1",
    ],
    install_requires=[
        "dlib==19.24.5",
        "onnxoptimizer==0.3.13",
        "onnxruntime==1.18.1",
        "opencv-contrib-python==4.10.0.84",
        "tqdm==4.66.5",
        "requests==2.32.3"
    ],
    classifiers=[
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'License :: OSI Approved :: Apache Software License',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/huseyindas/face-detectors/issues',
        'Source': 'https://github.com/huseyindas/face-detectors',
        'Documentation': 'https://github.com/huseyindas/face-detectors#documentation',
    },
    keywords=[
        'machine learning',
        'face',
        'detector',
        'face detection',
        'CNN',
        'dlib',
        'ultrafast',
        'HOG',
        'caffemodel',
    ],
    include_package_data=True,
)

setup(**attrs)
