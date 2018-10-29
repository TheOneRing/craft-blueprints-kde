# -*- coding: utf-8 -*-
# Copyright Filipe Azevedo <pasnox@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "Utility scripts for internationalizing XML."
        for ver in ["0.51.0"]:
            self.targets[ver] = f"https://launchpad.net/intltool/trunk/{ver}/+download/intltool-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"intltool-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.patchToApply['0.51.0'] = [
            ("0001-Perl-5-22-compatibility.patch", 1)
        ]
        self.defaultTarget = '0.51.0'


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

    def postInstall(self):
        return self.patchInstallPrefix([os.path.join(self.imageDir(), x) for x in ["dev-utils/bin/intltoolize"]],
                                       self.subinfo.buildPrefix,
                                       CraftCore.standardDirs.craftRoot())
