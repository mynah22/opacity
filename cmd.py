#!/usr/bin/python
import core
import userconfirm as uc
from argparse import ArgumentParser

#setting up command-line argument parsing
argp = ArgumentParser()
modegroup = argp.add_mutually_exclusive_group(required=True)
modegroup.add_argument('-e', '--encrypt',
                       help='\nEncrypts a file.', 
                       action ='store_true',default=False)

modegroup.add_argument('-d', '--decrypt', 
                       help='\nDecrypts a file.',
                       action ='store_true', default=False)

argp.add_argument('-p', '--passphrase', 
                  help ='\nONLY FOR TESTING.\n'
                  'passes passpharse on command line,\n'+
                  'and therefore may be recorded.')

argp.add_argument('-i','--inputpath', help='\nPath to input')

argp.add_argument('-o','--outputpath', help='\nPath to output.\n')

argp.add_argument('-r','--read',action ='store_true', default=False, 
                  help='\nRead file to stdout; do not save output.\n'+
                  'overrides -o')
arguments = argp.parse_args()
# get input path from user if not passed as argument
if not arguments.inputpath:
    inputpath = uc.getinputpath()
else:
    inputpath = arguments.inputpath
# get ouptut path / read option from user if not passed as argument
if not arguments.read:
    if not arguments.outputpath:
        outputtuple = uc.getoutputpath()
        if outputtuple[1]:
            if outputtuple[1].startswith('read'):
                arguments.read = True
            elif (outputtuple[1].startswith('new') or 
            outputtuple[1].startswith('over')):
                print('OVERWRITING FILE\n'+outputtuple[0]+'\n')
                outputpath = outputtuple[0]
    else:
        outputpath = arguments.outputpath
# get passphrase from user if not passed as argument
if not arguments.passphrase:
    passphrase = uc.getpassphrase()
else:
    passphrase = arguments.passphrase


if __name__ == '__main__':
    if arguments.encrypt:
        if arguments.read:
         with open(inputpath, 'rb') as infile:
          ddict=core.encrypt(passphrase, infile.read())
          for i in ddict: print(i+': '+str(ddict[i]))
        else:
          core.encryptfile(inputpath, outputpath, passphrase)
          print('file encryption over')
    elif arguments.decrypt:
        if arguments.read:
          pass
        else:
          core.decryptfile(inputpath, outputpath, passphrase)
          print('file decryption over')