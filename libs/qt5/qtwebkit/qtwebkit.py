# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["5.212"] = "https://code.qt.io/qt/qtwebkit.git|5.212"

        for ver in self.versionInfo.branches():
            if CraftVersion(ver) < "5.212":
                self.patchToApply[ver] = [("build-with-mysql.diff", 1),
                                          ("disable-icu-test.diff", 1)]

        self.patchToApply["5.212"] = [("qtwebkit-20181022.patch", 1),
                                      ("773.patch", 1), #https://github.com/annulen/webkit/pull/773
                                      ]
        self.patchToApply["dev"] = [("qtwebkit-20181022.patch", 1)]

        for ver in ["5.10", "5.11"]:
            self.svnTargets[ver] = self.svnTargets["5.212"]
            self.patchToApply[ver] = self.patchToApply["5.212"]

        # replace tarbals by git branches
        branchRegEx = re.compile("\d\.\d+\.\d+")
        for ver in self.versionInfo.tarballs():
            branch = branchRegEx.findall(ver)[0][:-2]
            del self.targets[ver]
            if ver in self.targetInstSrc:
                del self.targetInstSrc[ver]
            self.svnTargets[ver] = self.svnTargets[branch]
            self.patchToApply[ver] = self.patchToApply[branch]

        for ver in self.versionInfo.tags():
            branch = branchRegEx.findall(ver)[0][:-2]
            self.svnTargets[ver] = self.svnTargets[branch]
            self.patchToApply[ver] = self.patchToApply[branch]


    def setDependencies(self):
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = None
        self.runtimeDependencies["libs/qt5/qtsensors"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.buildDependencies["dev-utils/ruby"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/python2"] = None
        self.buildDependencies["dev-utils/nasm"] = None


from Package.Qt5CorePackageBase import *
from Package.CMakePackageBase import *


class QtPackage(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DPORT=Qt -DENABLE_API_TESTS=OFF -DENABLE_TOOLS=OFF " \
                                               "-DUSE_GSTREAMER=OFF " \
                                               "-DUSE_QT_MULTIMEDIA=ON -DUSE_MEDIA_FOUNDATION=OFF -DUSE_LIBHYPHEN=OFF"

    def fetch(self):
        if os.path.exists(self.sourceDir()):
            utils.system(["git", "reset", "--hard"], cwd=self.sourceDir())
        return super().fetch()


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
