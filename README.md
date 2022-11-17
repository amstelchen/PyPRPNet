[![Documentation Status](https://readthedocs.org/projects/pyprpnet/badge/?version=latest)](https://pyprpnet.readthedocs.io/en/latest/?badge=latest) [![Python package](https://github.com/amstelchen/PyPRPNet/actions/workflows/python-package-no-pytest.yml/badge.svg)](https://github.com/amstelchen/PyPRPNet/actions/workflows/python-package-no-pytest.yml)

<h1>PyPRPNet</h1>

### PyPRPNet is a library to control all aspects of the PRPNet client (https://prpnet.primegrid.com)

#### Introduction

TBD

#### Installation

Steps assume that `python` (>= 3.7) and `pip` are already installed.

Install from PyPI:

    $ pip install pyprpnet

or from the wheel:

    $ pip install pyprpnet-0.1.0-py3-none-any.whl

Install directly from ``github``:

    $ pip install git+https://github.com/amstelchen/PyPRPNet#egg=PyPRPNet


#### Usage

    >>> import pyprpnet as PRP

    >>> prp = PRP.PyPRPNet(client_path="/path/to/workdir")

    >>> print(prp.version())
    PyPRPNet 0.1.0 (64bit)
    MIT License
    Copyright (c) 2022 Michael John

    >>> prp.setup("john_doe@mail.com", "John_Doe", "hostname", "BOINC@Team")

    >>> prp.install()

    >>> for key, value in prp._get_config().items():
    ...     print(f'{key:14s} : {value}')
    email          : john_doe@mail.com
    userid         : John_Doe
    machineid      : hostname
    instanceid     : INSTANCE_ID
    teamid         : BOINC@Team
    server         : FPS:0:1:prpnet.primegrid.com:12002
    llrexe         : ./llr
    pfgwexe        : ./pfgw64
    wwwwexe        : ./wwww
    cpuaffinity    : 
    gpuaffinity    : 
    normalpriority : 0
    startoption    : 3
    stopoption     : 3
    stopasapoption : 0
    errortimeout   : 3
    loglimit       : 1
    debuglevel     : 0
    echotest       : 1

    prp.start_all()

    prp.stop_all()

    prp.start_slot(1)

    for s in prp.status():
        print(s)
    {'WorkUnit': '1668523703 300574!-1', 'Status': 'running', 'Progress': '2912500/5036027', 'Percent': '57.83%', 'Slot': 1}
    ...

    prp.workunits()
    ServerName=prpnet.primegrid.com
    PortID=12002
    ServerVersion=5.4.3
    ServerType=6
    Start WorkUnit 1668541419 300594!-1 0 300594 0 -1 0
    Main: 300594!-1 inprogress na na na na 2 -1 0 0.000000 0
    End WorkUnit 1668541419 300594!-1
    ...


#### Reporting bugs

If you encounter any bugs or incompatibilities, __please report them [here](https://github.com/amstelchen/PyPRPNet/issues/new)__.

#### Future plans / TODO

TBD, (see TODO.md)

#### Licences

*PyPRPNet* is licensed under the [MIT](LICENSE) license.
