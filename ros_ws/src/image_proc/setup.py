from setuptools import find_packages, setup
import os
package_name = 'image_proc'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ted Lin',
    maintainer_email='ptengineerlin@gmail.com',
    description='Image processing node',
    license='Apache Lincense 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_proc_node = image_proc.image_proc_node:main'
        ],
    },
)
