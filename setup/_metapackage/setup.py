import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-git",
    description="Meta package for open-synergy-ssi-git Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_git',
        'odoo14-addon-ssi_git_server_action',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
