__licence__ = "MIT License"
__copyright__ = "Copyright (c) 2022, 2023 Michael John"
__version__ = "0.2.0"

import pyprpnet as PRP

prp = PRP.PyPRPNet(client_path="/home/mic/Downloads/prpclient-5.4.0a-linux_64/")
print(prp.version())
prp.setup("amstelchen@gmx.at", "Michael_John", "sundance", "BOINC@Austria")
#prp.install()             # ok
#print(prp._path)            # ok
#print(prp.get_all())       # ok
#print(prp._get_config())   # ok
for key, value in prp._get_config().items():
    print(f'{key:14s} : {value}')
#print(prp.get_user())      # ok
#prp.stop_all()            # ok
#prp.start_slot(1)              # ok
#prp.start_all()            # ok
for s in prp.status():
    print(s)
#for w in prp.workunits():
#    print(w)
#print(prp.workunits())
#print(prp.status())
