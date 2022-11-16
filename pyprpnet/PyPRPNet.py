'''===========================================================================
MIT License

Copyright (c) 2022 Michael John

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==========================================================================='''

import os
import sys
import shutil
import requests
import json
from typing import Dict, List
import py7zr
from time import sleep
from subprocess import Popen, DEVNULL
from psutil import cpu_count
from natsort import natsorted, ns

__licence__ = "MIT License"
__copyright__ = "Copyright (c) 2022 Michael John"
__version__ = "0.1.0"

def is_64bit() -> bool:
    """check if running platform is 64bit python."""
    return sys.maxsize == 9223372036854775807


class PyPRPNet:
    """
    See the <a href="https://github.com/amstelchen/PyPRPNet">GitHub repository</a> for more information about the development.
    """
    def __init__(self, client_path: str):
        """
        Sets up a valid PRPNet object.

        :param username: of the current user (not None).<br>
        :param password: for the current user (not None).<br>
        :param client_path: path to the client.
        """
        assert client_path is not None
        """Path to the client."""
        self._path = client_path

    def setup(self, email: str, userid: str, machineid = "", teamid = "") -> None:
        """
        Set some user credentials.

        :param email: email= is a REQUIRED field.  The server will use this address<br>to send you an e-mail when your client discovers a prime.<br>
        :param userid: userid= is a REQUIRED field that will be used by the server<br>to report on stats, etc.
        :param machineid: This value differentiates clients using the same e-mail ID<br>
        :param teamid: Tests completed by this "team" will be rolled-up as part of team stats.
        :return: TBD.
        """
        assert email is not None
        assert userid is not None
        self._email = email
        self._userid = userid
        self._machineid = str(machineid)
        self._teamid = str(teamid)
        return

    def version(self) -> str:
        """
        A simple message with version info returned.
        """
        return self.__class__.__name__ + " " + __version__ + \
            " (" + ("64bit" if is_64bit() else "32bit") + ")" + \
            "\n" + __licence__ + "\n" + __copyright__ + "\n"

    def install(self):
        """
        Downloads and installs the PRPNet client and proper slots.
        """
        if not os.path.isdir(self._path):
            os.mkdir(self._path)
            os.mkdir(os.path.join(self._path, 'slots'))
            os.mkdir(os.path.join(self._path, 'programs'))
        
        if is_64bit:
            client = 'prpclient-5.4.0a-linux_64'
        else:
            client = 'prpclient-5.4.0a-linux_32'
        filename = os.path.join(self._path, 'programs', client + '.7z')

        targets = [client + '/programs/llr', 
                    client + '/programs/pfgw64', 
                    client + '/programs/prpclient', 
                    client + '/programs/wwww', 
                    client + '/programs/wwwwcl']

        if not os.path.exists(filename):
            url = "https://prpnet.primegrid.com/software/" + client + '.7z'
            req = requests.get(url)
            with open(filename, 'wb') as fd:
                for chunk in req.iter_content(chunk_size=128):
                    fd.write(chunk)

        with py7zr.SevenZipFile(filename, mode='r') as z:
            allfiles = z.getnames()
            #print(allfiles)
            z.extract(path=os.path.join(self._path, 'programs'), targets=targets)
        with py7zr.SevenZipFile(filename, mode='r') as z:
            z.extract(path=os.path.join(self._path, 'programs'), targets=[client + '/master_prpclient.ini'])
        for target in targets:
            try:
                os.rename(os.path.join(self._path, 'programs', target), os.path.join(self._path, 'programs', os.path.basename(target)))
            except OSError():
                pass
        os.rename(os.path.join(self._path, 'programs', client, 'master_prpclient.ini'), os.path.join(self._path, 'master_prpclient.ini'))
        os.rmdir(os.path.join(self._path, 'programs', client, 'programs'))
        os.rmdir(os.path.join(self._path, 'programs', client))

        self._set_config()

        for slot in range(1, cpu_count() + 1):
            os.mkdir(os.path.join(self._path, 'slots', str(slot)))
            for target in targets:
                shutil.copy(os.path.join(self._path, 'programs', os.path.basename(target)), os.path.join(self._path, 'slots', str(slot)))
                shutil.copy(os.path.join(self._path, 'master_prpclient.ini'), os.path.join(self._path, 'slots', str(slot), "prpclient.ini"))
                os.system("sed -i s/INSTANCE_ID/"+ str(slot) + "/ " + os.path.join(self._path, 'slots', str(slot), "prpclient.ini"))
        
    def workunits(self) -> List[dict]:
        """
        Returns all workunits of the clients that are setup.

        :return: all workunits of the clients that are setup.
        """
        #assert api_part is not None
        #api_url: str = api_part + '/slots'
        res = []
        for path in os.listdir(os.path.join(self._path, 'slots')):
            # check if current path is a file
            if os.path.isdir(os.path.join(self._path, 'slots', path)):
                #print(os.path.join(self._path, 'slots', path))
                file = os.path.join(self._path, 'slots', path, 'work_FPS.save')
                if os.path.isfile(file):
                    with open(file, "rt") as workfile:
                        for line in workfile.readlines():
                            print(line.strip())
                #res.append(path)
        return res

    def status(self) -> List[dict]:
        """
        Returns all workunits of the clients that are setup, but as a dictionary.

        :return: all workunits of the clients that are setup, but as a dictionary.
        """
        #assert api_part is not None
        #api_url: str = api_part + '/slots'
        res = []
        for path in natsorted(os.listdir(os.path.join(self._path, 'slots')), alg=ns.PATH | ns.IGNORECASE):
            # check if current path is a file
            if os.path.isdir(os.path.join(self._path, 'slots', path)):
                #print(os.path.join(self._path, 'slots', path))
                file = os.path.join(self._path, 'slots', path, 'work_FPS.save')
                lock = os.path.join(self._path, 'slots', path, 'client.lock')
                if os.path.isfile(lock):
                    status = "running"
                else:
                    status = "stopped"
                if os.path.isfile(file):
                    with open(file, "rt") as workfile:
                        for line in workfile.readlines():
                            if line.startswith("End"):
                                #print(line.strip())
                                res.append({"WorkUnit": line.strip("End WorkUnit ").strip(), "Status": status, "Slot": int(path)})
        return res

    def get_user_old(self) -> int:
        """
        Returns the id of the user, old way.

        :return: id of the user.
        """
        file = os.path.join(self._path, 'master_prpclient.ini')
        if os.path.isfile(file):
            with open(file, "rt") as conffile:
                for line in conffile.readlines():
                    #if not line.startswith("//"):
                    if line.startswith("userid"):
                        return line.strip()

    def get_user(self) -> int:
        """
        Returns the id of the user, via _get_config().

        :return: id of the user.
        """
        for line in self._get_config():
            if "userid" in line:
                return line.split("=")[1]

    def _get_config(self):
        """
        Gets a list of strings from the configuration file.

        :return: a list of strings from the configuration file.
        """
        #cnf = []
        cnf = {}
        file = os.path.join(self._path, 'master_prpclient.ini')
        if os.path.isfile(file):
            with open(file, "rt") as conffile:
                for line in conffile.readlines():
                    if not line.startswith("//") and len(line.strip()) > 0:
                        #cnf.append(line.strip())
                        line = line.strip()
                        cnf[line.split("=")[0]] = line.split("=")[1]
                return cnf

    def _set_config(self) -> None:
        """
        Updates the strings to the configuration file.

        :return: None.
        """
        cnf = []
        file = os.path.join(self._path, 'master_prpclient.ini')
        if os.path.isfile(file):
            with open(file, "rt") as conffile:
                contents = conffile.readlines()
            
            for line_nr, line in enumerate(contents):
                if not line.startswith("//") and len(line.strip()) > 0:
                    if line.startswith("email="):
                        contents[line_nr] = "email=" + self._email + "\n"
                    if line.startswith("userid="):
                        contents[line_nr] = "userid=" + self._userid + "\n"
                    if line.startswith("machineid="):
                        contents[line_nr] = "machineid=" + self._machineid + "\n"
                    if line.startswith("teamid="):
                        contents[line_nr] = "teamid=" + self._teamid + "\n"

            with open(file, "wt") as conffile:
                conffile.writelines(contents)

                return cnf

    def stop_all(self):
        """
        Stops all running clients.

        :return: TBD.
        """
        targets = ["llr", "pfgw64", "genefer", "genefer80", "genefercuda", "genefx64", "wwww", "wwwwcl"]
        for victim in targets:
            #os.system("killall -2 " + victim)
            Popen(["killall", "-", victim], shell=False, stdout=DEVNULL, stderr=DEVNULL)
        sleep(5)
        #os.system("killall -2 prpclient")
        Popen(["killall", "-", "prpclient"], shell=False, stdout=DEVNULL, stderr=DEVNULL)

    def start_slot(self, slot: int) -> int:
        """
        Starts a client in the specified slot.

        :param slot: a slot number.
        :return: TBD.
        """
        slotpath = os.path.join(self._path, 'slots', str(slot))
        if os.path.isdir(slotpath):
            os.chdir(slotpath)
            #return os.system("./prpclient")
            Popen("./prpclient", shell=False, stdout=DEVNULL, stderr=DEVNULL)

    def start_all(self):
        """
        Starts the maximum number of clients.

        :return: TBD.
        """
        for slot in range(1, cpu_count() + 1):
            slotpath = os.path.join(self._path, 'slots', str(slot))
            if os.path.isdir(slotpath):
                os.chdir(slotpath)
                #return os.system("./prpclient")
                Popen("./prpclient", shell=False, stdout=DEVNULL, stderr=DEVNULL)
