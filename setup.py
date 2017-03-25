from setuptools import setup, find_packages


exclude = ['sentinella.sentinella-kvm.sentinella-kvm']

install_requires = ['trollius==2.0', 'libvirt-python==3.1.0']

setup(
    name='sentinella-kvm',
    description='Get metrics for KVM',
    version='0.1',
    packages=find_packages(exclude=exclude),
    zip_safe=False,
    namespace_packages=['sentinella'],
    install_requires=install_requires,
    author='Julio Acuña',
    author_email='urkonn@gmail.com',
    url='https://github.com/urkonn/sentinella-kvm',
    license='ASF',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Monitoring',
    ],
    keywords='monitoring metrics agent openstack sentinella',
)
