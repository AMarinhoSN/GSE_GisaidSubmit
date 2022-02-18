from setuptools import setup

setup(
    name="GSE_GisaidSubmit",
    version="0.1.dev",
    description="""
      handling tools used at genomic surveillance at Aggeu Magalhaes Institute
      """,
    url="https://github.com/AmarinhoSN/GSE_GisaidSubmit/",
    author='"Antonio Marinho da Silva Neto',
    author_email="amarinhosn@pm.me",
    # packages=["gse_gisaidsubmit"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    scripts=[
        "scripts/IAM_feedTabelao",
        "scripts/IAM_getToSubmitDF_gis",
        "scripts/IAM_getUp2GisaidFiles",
        "scripts/IAM_getGIS2IAM"
    ],
    install_requires=["pandas"],
    zip_safe=False,
)
