from setuptools import setup


setup(name='hd_glio',
      version='1.4',
      packages=["hd_glio"],
      description='Tool for brain tumor segmentation. This is the result of a joint project between the Department of '
                  'Neuroradiology at the Heidelberg University Hospital and the Division of Medical Image Computing at '
                  'the German Cancer Research Center (DKFZ). See readme.md for more information',
      url='https://github.com/MIC-DKFZ/hd_glio',
      python_requires='>=3.5',
      author='Fabian Isensee',
      author_email='f.isensee@dkfz.de',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
          'torch',
          'numpy',
          'scikit-image',
          'SimpleITK',
          'batchgenerators'
      ],
      entry_points={
          'console_scripts': [
                'hd_glio_predict = hd_glio.hd_glio_predict:main',
                'hd_glio_predict_folder = hd_glio.hd_glio_predict_folder:main',
        ],
      },
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Operating System :: Unix'
      ]
      )

