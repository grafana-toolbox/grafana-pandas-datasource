###############################
Grafana pandas datasource setup
###############################


************
Introduction
************

Until this package will provide an appropriate entrypoint program, it is
recommended to install it from the source repository.


*******************
Sandbox environment
*******************

In order to work efficiently with the resources provided by this repository, we
recommend to install some programs upfront. This will optimally work on Linux
and macOS. Windows users might use the WSL subsystem, and follow the
instructions for Ubuntu.


Install prerequisites
=====================
::

    # macOS / Homebrew
    brew install git python3 poetry httpie docker

    # Debian and Ubuntu
    apt update
    apt install --yes git python3 python3-pip httpie docker.io
    pip install poetry

    # Arch Linux
    pacman --sync --refresh
    pacman --noconfirm --sync git python3 poetry httpie docker

    # Fedora
    dnf install -y git python3 poetry httpie docker
    alternatives --install /usr/bin/python python /usr/bin/python3 1

    # Rocky Linux
    dnf install -y git python39 python39-pip docker
    pip3 install poetry httpie

    # CentOS 7
    yum install -y git docker
    yum -y install centos-release-scl-rh centos-release-scl
    yum --enablerepo=centos-sclo-rh -y install rh-python38
    scl enable rh-python38 bash
    pip3 install cryptography==3.3.2 poetry httpie

    # CentOS 8
    dnf install -y git python39 python39-pip docker
    pip3 install poetry httpie

    # openSUSE
    zypper install git python39 python39-pip httpie docker
    pip3.9 install poetry

    # Windows / Chocolatey
    # https://chocolatey.org/
    choco install git python3 poetry httpie docker-desktop docker-cli


Acquire sources
===============
::

    git clone https://github.com/panodata/grafana-pandas-datasource
    cd grafana-pandas-datasource


Bootstrap sandbox
=================
::

    python3 -m venv .venv

    # Linux, *nix, macOS
    source .venv/bin/activate

    # Windows
    .\venv\Scripts\activate

    pip install poetry
    poetry install
    poetry shell
