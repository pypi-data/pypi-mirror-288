from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='sci_plot_style',
    version='1.0.3',
    classifiers=[
        'Development Status :: 3 - Alpha', 'Environment :: Console',
        'Operating System :: OS Independent'
    ],
    license='GPLv3',
    description='SCI style',
    long_description_content_type="text/markdown",
    long_description=readme,
    author='Feifeng Wu',
    author_email='wufeifeng_hust@163.com',
    keywords=['matplotlib'],
    python_requires=">=3.6",
    install_requires=['matplotlib'],
    packages=find_packages(),
    package_data={
      'sci_plot_style': ['styles/**/*.mplstyle', 'styles/**/*.ttf'],
    },
    include_package_data=True,
)