# Development

## Tools 
- Python
- Ansible
- Linux OS


[Linux]
virtualenv venv
source venv/bin/activate


[Windows]
venv\Scripts\activate


TESS HTML: 
http://htmlpreview.github.com/?https://github.com/VDL-PRISM/TESS/blob/master/docs/index.html


## Create docs for TESS
cd TESS
python setup.py docs

delete all api files to create documents



pip install pyscaffold
pip freeze
putup TESS

less requirements.txt

python setup.py install
git tag -a v0.1 -m “first”

gitk.cmd --all
python setup.py sdist
python setup.py bdist
python setup.py test

pip install sphinx
python setup.py docs
