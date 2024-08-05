from setuptools import setup

setup(name='kla_first_distributions',
      
      version='0.86',
      
      description='Gaussian and Binomial distributions',
      
      packages=['kla_first_distributions'],

      author = 'KA',

      author_email= "myemail@somthing.com",

      long_description=open('README.md').read(),  # This can be used for a more detailed description,
      long_description_content_type='text/markdown',  # Specify the format of your long description,

      zip_save=False)