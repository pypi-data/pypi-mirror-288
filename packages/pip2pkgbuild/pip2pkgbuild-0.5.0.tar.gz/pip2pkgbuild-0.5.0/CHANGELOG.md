# Changelog


## 0.5.0 (2024-08-06)
- Replace imp by importlib, Python 3 defaults to PEP517 packaging by [@hseg](https://github.com/hseg).


## 0.3.9 (2024-02-21)
- Fix Python2 compatibility issue again ...


## 0.3.8 (2024-02-21)
- Fix Python2 compatibility issue.


## 0.3.7 (2024-02-21)
- Fix determining known licenses according to [RFC16](https://rfc.archlinux.page/0016-spdx-license-identifiers/) by [@hseg](https://github.com/hseg).


## 0.3.6 (2023-12-06)
- Add python-wheel as mkdepend for PEP517 based package.
- Disable PEP517 based PKGBUILD generation for Python 2 packages.


## 0.3.5 (2023-11-27)
- Fix issue of accessing extracted source folder.


## 0.3.4 (2023-09-14)
- Allow generation of PEP517 PKGBUILDs for Python modules without pyproject.toml.


## 0.3.3 (2023-03-01)
- Fix source archive file naming issue.


## 0.3.2 (2022-02-24)
- Fix license installation.


## 0.3.1 (2022-02-22)
- Fix incorrect brackets escape in license installation statement.


## 0.3.0 (2022-02-22)
- Support PEP517 based installation instructments.


## 0.2.6 (2019-04-13)
- Use SHA256 checksum.


## 0.2.5 (2019-04-13)
- Update SOURCE_TARGZ to match arch package guidelines, by @davve
- Avoid using array as pkgbase


## 0.2.4 (2017-06-10)
- Update pypi URL, by @mvdnes


## 0.2.3 (2016-12-17)
- Option for adding maintainer info, by @brycepg
- Option for installing license file, by @brycepg
- Fix source URL generation


## 0.2.2 (2016-11-27)
- Use "https://files.pythonhosted.org/" based source URL


## 0.2.1 (2016-05-22)
- Handle specified version of Python module not be found


## 0.2.0 (2016-05-21)
- Move package build process into build() function


## 0.1.5 (2015-10-06)
- Bug fixes


## 0.1.4 (2015-09-18)
- Package's Python version defaults to pip2pkgbuild's


## 0.1.3 (2015-09-16)
- Fix a Python 2 packaging error


## 0.1.2 (2015-09-16)
- Improve Python 2 compatibility


## 0.1.1 (2015-09-15)
- Re-structure project to fix packaging error


## 0.1.0 (2015-09-15)
- Initial release
