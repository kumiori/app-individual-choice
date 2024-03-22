from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-qualitative-selector",
    version="0.0.2",
    author="Andrés A León Baldelli",
    author_email="leon.baldelli@cnrs.fr",
    description="Choice, expanded with qualitative widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://individual-choice.streamlit.app/",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.20", "streamlit-extras>=0.1.0", "streamlit-survey>=0.1.0", "st-supabase-connection>=0.1.0"],
)