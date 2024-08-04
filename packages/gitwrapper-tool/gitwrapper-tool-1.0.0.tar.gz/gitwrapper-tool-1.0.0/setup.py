from setuptools import setup, find_packages
package_name = 'gitwrapper-tool'
package_version = '1.0.0'
autor_name = 'smit patel'
author_email = 'smit.dpatel9924@gmail.com'
maintainer_name = 'smit patel'
maintainer_email = 'smit.dpatel9924@gmail.com'
package_home_page_url = ''
package_short_description = ''
package_long_description = ''
package_download_url = ''
classifiers = [
    'Development Status :: 1 - Planning',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.10',
    'Topic :: Software Development :: Version Control',
]
platforms = []
keywords = []
package_license = 'MIT'

package_id = {'' : 'src'}
packages = find_packages()
entry_points = {
    'console_scripts': [
        'gitwrapper = gitwrapper.main:main'
    ] 
}

setup(
    name = package_name,
    version = package_version,
    author = autor_name,
    author_email = author_email,
    maintainer = maintainer_name,
    maintainer_email = maintainer_email,
    url = package_home_page_url,
    classifiers = classifiers,
    description = package_short_description,
    long_description = package_long_description,
    download_url = package_download_url,
    platforms = platforms,
    keywords = keywords,
    license = package_license,
    packages = packages,
    entry_points = entry_points
)