from setuptools import setup

setup(name='eds_ds_tools',
      version='0.1',
      description='tools for data',
      packages=['eds_ds_tools'],
      author_email='wenleicao@gmail.com',
      zip_safe=False,
      install_requires=[
      'boto3', 'botocore', 'numpy', 'pandas', 'pytz', 'requests'
      ]
      )
