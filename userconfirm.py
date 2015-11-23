#!/usr/bin/python
import getpass, os
def getpassphrase():
    passconfirmed = False
    while not passconfirmed:
        pphr = getpass.getpass('Enter your passphrase\n')
        if pphr == getpass.getpass('Confirm passphrase\n'):
            passconfirmed = True
        else:
            print('Passphrases do not match.\n')
    return pphr
def getinputpath():
    ipathconfirmed = False
    while not ipathconfirmed:
        ipath = raw_input('Enter input file path\n')
        if os.path.exists(ipath):
            ipathconfirmed = True
        else:
            print('Path does not exist.\n')
    return ipath
    
def getoutputpath():
    opathconfirmed = False
    newf = False
    while not opathconfirmed:
        opath = raw_input('Enter output path\n(R to read to console)\n')
        if opath.lower() == 'r':
            rvals = (None, 'read')
            opathconfirmed = True
        elif os.path.exists(opath):
            inp0 = raw_input('Path is occupied.\n'
                            'Overwite present file?\n'
                            '(Y for yes, N for no,'
                            +' C to cancel and exit.)\n')
            if inp0.lower() == 'y':
                rvals = (opath, 'over')
                opathconfirmed = True
            elif inp0.lower == 'n':
                print('\n\n')
            elif inp0.lower == 'c':
                exit()
        else:
            inp1 = raw_input('Path does not exist.\n'
                            'Create new file?\n'
                            '(N for new file at '+opath+',\n'
                            +'C to cancel and exit.)\n')
            if inp1.lower() == 'n':
                opathconfirmed = True
                rvals = (opath, 'new')
            elif inp1.lower() == 'c':
                exit()
    return rvals
