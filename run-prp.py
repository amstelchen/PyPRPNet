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
#prp.start(1)              # ok
#prp.start_all()            # ok
for s in prp.status():
    print(s)
