from os import system

clean = 'make clean'
source = 'sphinx-apidoc -o sources ../b3j0f'
html = 'make html'

system(clean) or system(source) or system(html)
