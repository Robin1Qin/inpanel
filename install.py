#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - 2018, doudoudzj
# Copyright (c) 2012 - 2016, VPSMate development team
# All rights reserved.
#
# Intranet is distributed under the terms of The New BSD License.
# The full license can be found in 'LICENSE'.

""" Install Script for Intranet """

import getpass
import os
import platform
import shlex
import socket
import subprocess
# import urllib2
import sys
# import re

class Install(object):
    def __init__(self):

        self.user = getpass.getuser()

        if (self.user != 'root'):
            print('Must run in root')
            sys.exit()

        if hasattr(platform, 'linux_distribution'):
            self.dist = platform.linux_distribution(full_distribution_name=0)
        else:
            self.dist = platform.dist()
        self.arch = platform.machine()
        if self.arch != 'x86_64':
            self.arch = 'i386'
        self.installpath = '/usr/local/intranet'
        self.intranet_port = 8888
        self.repository = 'https://github.com/intranet-panel/intranet.git'
        self.distname = self.dist[0].lower()
        self.version = self.dist[1]
        self.version = self.version[0:self.version.find('.', self.version.index('.') + 1)]
        self.os = platform.system()
        print('Platform %s %s [%s]' % (self.dist[0], self.dist[1], self.os))

    def _run(self, cmd, shell=False):
        if shell:
            return subprocess.call(cmd, shell=shell)
        else:
            return subprocess.call(shlex.split(cmd))

    def check_platform(self):
        supported = True
        if self.distname == 'centos':
            if float(self.version) < 5.4:
                supported = False
        elif self.distname == 'redhat':
            if float(self.version) < 5.4:
                supported = False
        elif self.os == 'Darwin':
            supported = True
        # elif self.distname == 'ubuntu':
        #    if float(self.version) < 10.10:
        #        supported = False
        # elif self.distname == 'debian':
        #    if float(self.version) < 6.0:
        #        supported = False
        else:
            supported = False
        return supported

    def check_git(self):
        supported = True
        try:
            if self.distname in ('centos', 'redhat'):
                self._run("yum install -y git")
        except:
            pass

        if self.distname == 'centos':
            if float(self.version) < 5.4:
                supported = False
        elif self.distname == 'redhat':
            if float(self.version) < 5.4:
                supported = False
        elif self.os == 'Darwin':
            supported = True
        elif self.distname == 'ubuntu':
           if float(self.version) < 10.10:
               supported = False
        elif self.distname == 'debian':
           if float(self.version) < 6.0:
               supported = False
        else:
            supported = False
        return supported

    def install_epel_release(self):
        if self.distname in ('centos', 'redhat'):
            # following this: http://fedoraproject.org/wiki/EPEL/FAQ
            if int(float(self.version)) == 5:
                epelrpm = 'epel-release-5-4.noarch.rpm'
                epelurl = 'http://download.fedoraproject.org/pub/epel/5/%s/%s' % (self.arch, epelrpm)
                # install fastestmirror plugin for yum
                fastestmirror = 'http://mirror.centos.org/centos/5/os/%s/CentOS/yum-fastestmirror-1.1.16-21.el5.centos.noarch.rpm' % (self.arch)
                self._run('rpm -Uvh %s' % fastestmirror)
            elif int(float(self.version)) == 6:
                epelrpm = 'epel-release-6-8.noarch.rpm'
                epelurl = 'https://mirrors.aliyun.com/epel/6/%s/%s' % (self.arch, epelrpm)
                fastestmirror = 'https://mirrors.aliyun.com/centos/6/os/%s/Packages/yum-plugin-fastestmirror-1.1.30-41.el6.noarch.rpm' % (self.arch)
                # fastestmirror = 'http://mirror.centos.org/centos/6/os/%s/Packages/yum-plugin-fastestmirror-1.1.30-41.el6.noarch.rpm' % (self.arch)
                self._run('rpm -Uvh %s' % fastestmirror)
            elif int(float(self.version)) == 7:
                epelrpm = 'epel-release-7-11.noarch.rpm'
                epelurl = 'https://mirrors.aliyun.com/epel/7/%s/Packages/e/%s' % (self.arch, epelrpm)
                fastestmirror = 'https://mirrors.aliyun.com/centos/7/os/%s/Packages/yum-plugin-fastestmirror-1.1.31-45.el7.noarch.rpm' % (self.arch)
                # fastestmirror = 'http://mirror.centos.org/centos/7/os/%s/Packages/yum-plugin-fastestmirror-1.1.31-45.el7.noarch.rpm' % (self.arch)
                self._run('rpm -Uvh %s' % fastestmirror)

            self._run('wget -nv -c %s' % epelurl)
            self._run('rpm -Uvh %s' % epelrpm)
            print('OK')

    def install_python(self):
        if self.distname == 'centos':
            self._run('yum -y install python26')

        elif self.distname == 'redhat':
            self._run('yum -y install python26')

        elif self.distname == 'ubuntu':
            pass

        elif self.distname == 'debian':
            pass

    def handle_intranet(self):
        # handle Intranet
        # get the latest Intranet version
        print('* Installing Intranet')
        # localpkg_found = False
        # if os.path.exists(os.path.join(os.path.dirname(__file__), 'intranet.tar.gz')):
        #     # local install package found
        #     localpkg_found = True
        # else:
        #     # or else install online
        #     print('* Downloading install package from intranet.pub')
        #     f = urllib2.urlopen('http://api.intranet.pub/?s=latest')
        #     data = f.read()
        #     f.close()
        #     downloadurl = re.search('"download":"([^"]+)"', data).group(1).replace('\/', '/')
        #     self._run('wget -nv -c "%s" -O intranet.tar.gz' % downloadurl)
        
        # # uncompress and install it
        # self._run('mkdir intranet')
        # self._run('tar zxmf intranet.tar.gz -C intranet  --strip-components 1')
        # if not localpkg_found: os.remove('intranet.tar.gz')

        # stop service
        if os.path.exists('/etc/init.d/intranet'):
            self._run('/etc/init.d/intranet stop')

        # backup data and remove old code
        # if os.path.exists('%s/data/' % self.installpath):
        #     self._run('mkdir /tmp/intranet_panel_data', True)
        #     self._run('/bin/cp -rf %s/data/* /tmp/intranet_panel_data/' % self.installpath, True)

        self._run('rm -rf %s' % self.installpath)
        branch = 'master'
        if len(sys.argv) == 2 and sys.argv[1] == '--dev':
            branch = 'dev'
        self._run('git clone -b %s %s %s' % (branch, self.repository, self.installpath))

        # install new code
        # self._run('mv intranet %s' % self.installpath)
        self._run('chmod +x %s/config.py %s/server.py' % (self.installpath, self.installpath))

        # install service
        initscript = '%s/tools/init.d/%s/intranet' % (self.installpath, self.distname)
        self._run('cp %s /etc/init.d/intranet' % initscript)
        self._run('chmod +x /etc/init.d/intranet')

    def config_firewall(self):
        # config firewall
        print('* Config iptables')
        if os.path.exists('/etc/init.d/iptables'):
            self._run('iptables -A INPUT -p tcp --dport %s -j ACCEPT' % self.intranet_port)
            self._run('iptables -A OUTPUT -p tcp --sport %s -j ACCEPT' % self.intranet_port)
            self._run('service iptables save')
            self._run('/etc/init.d/iptables restart')

    def config_account(self):
        # set username and password
        username = raw_input('Admin username [default: admin]: ').strip()
        password = raw_input('Admin password [default: admin]: ').strip()
        if len(username) == 0:
            username = 'admin'
        if len(password) == 0:
            password = 'admin'

        self._run('%s/config.py username "%s"' % (self.installpath, username))
        self._run('%s/config.py password "%s"' % (self.installpath, password))

        print('* Username and password set successfully!')

    def detect_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('www.baidu.com', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def handle_vpsmate(self):
        # handle VPSMate

        if os.path.exists('/etc/init.d/vpsmate'):
            print('* Checking VPSMate')
            isdel = raw_input('Delete VPSMate ? [yes or no, default: yes]: ').strip()
            if len(isdel) == 0:
                isdel = 'yes'
            if isdel == 'yes':
                self._run('/etc/init.d/vpsmate stop')
                self._run('rm -f /etc/init.d/vpsmate')
                self._run('rm -rf /usr/local/vpsmate')
                print('* VPSMate has been deleted')
            else:
                if not isdel == 'no':
                    print('* The command you entered is incorrect !')
                self.intranet_port = 8899
                self._run('%s/config.py port "%s"' % (self.installpath, self.intranet_port))
                print('* Intranet and VPSMate now can run simultaneously !')

    def start_service(self):
        # start service
        if self.distname in ('centos', 'redhat'):
            self._run('chkconfig intranet on')
            self._run('service intranet start')
        elif self.distname == 'ubuntu':
            pass
        elif self.distname == 'debian':
            pass

    def install(self):
        # check platform environment
        print('* Checking platform...'),
        supported = self.check_platform()

        if not supported:
            print('FAILED')
            print('Unsupport platform %s %s %s' % self.dist)
            sys.exit()
        else:
            print(self.distname),
            print('...OK')

        print('* Install depend software ...')
        self._run('yum install -y wget net-tools vim psmisc rsync libxslt-devel GeoIP GeoIP-devel gd gd-devel')

        print('* Install EPEL release...'),
        self.install_epel_release()

        # check python version
        print('* Current Python version [%s.%s] ...' % (sys.version_info[:2][0], sys.version_info[:2][1])),

        if (sys.version_info[:2] == (2, 6) or sys.version_info[:2] == (2, 7)):
            print('OK')
        else:
            print('FAILED')

            # install the right version
            print('* Installing python 2.6 ...'),
            self.install_python()

        # check GIT version
        print('* Checking GIT ...'),
        if self.check_git():
            print('OK')
        else:
            print('FAILED')

        # if sys.version_info[:2] == (2, 6):
        #     print('OK')
        # else:
        #     print('FAILED')
        #
        #     # install the right version


        #     print '* Installing python 2.6 ...'
        #     self.install_python()

        self.handle_intranet()
        self.handle_vpsmate()
        self.config_account()
        self.config_firewall()
        self.start_service()

        print
        print
        print('============================')
        print('*    INSTALL COMPLETED!    *')
        print('============================')
        print
        print

        print('* The URL of your Intranet Panel is:'),
        print('http://%s:%s/' % (self.detect_ip(), self.intranet_port))
        print
        print

        pass


def main():
    install = Install()
    install.install()


if __name__ == "__main__":
    main()