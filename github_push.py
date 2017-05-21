import subprocess
import warnings
from getpass import getpass

def sh(cmdline):
    """run cmd in a subprocess and return its output.
    raises RuntimeError on error.
    """
    p = subprocess.Popen(cmdline, shell=1, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(stderr.decode('UTF-8'))
    if stderr:
        warnings.warn(stderr.decode('UTF-8'), RuntimeWarning)
    return stdout.decode('UTF-8')

#stato del repo
status = sh('git status')
for line in status.splitlines():
    if any([x in line for x in ['Changes', 'Untracked files:', '\t']]): print(line)


#inserimento commit
messag = input("inserisci messaggio di commit: ")
try:
    output = sh(f"""git commit --all -m '{messag}'""")
except RuntimeError:
    output = sh(f"""git commit --all --amend -m '{messag}'""")
print(output)

#inserimento nome e password
#nome = input("nome: ")
#print('\033[1A{}'.format(" "*(6+len(nome))), '\033[1A')
#pswd = input("pass: ")
#print('\033[1A{}'.format(" "*(6+len(pswd))), '\033[1A')
#print('ok')
addr = sh('git config --get remote.origin.url') #oppure "git remote show origin"
nome = getpass("nome: ")
pswd = getpass("pass: ")
addr = addr.split('//')
addr.insert(1, f"""//{nome}:{pswd}@""")
addr = ''.join(addr) 

##faccio un pull perché continua a rompere i coglioni, nun funziona
#pull = sh('git pull')

#costretto ad aggiungere il force per disperazione
output = sh(f"""git push {addr}""")
print(output)
