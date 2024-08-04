from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mebularts",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[],
    author="Mehmet Bulat",
    author_email="info@mebularts.com.tr",
    description=(
        "TR: @mebularts tarafından ♥ ile kodlanmıştır. Sahte Türk isim, soyisim, "
        "kullanıcı adı, adres, telefon numarası, doğum tarihi, şirket adı, email ve "
        "user_agent üretmek için ücretsiz bir kütüphane. "
        "EN: Coded with ♥ by @mebularts. A free library to generate fake Turkish names, "
        "surnames, usernames, addresses, phone numbers, dates of birth, company names, "
        "emails and user_agents."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mebularts.com.tr/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
