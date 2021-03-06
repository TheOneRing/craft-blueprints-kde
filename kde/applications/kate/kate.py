import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["18.08.1"] = 1

        self.displayName = "Kate"
        self.description = "the KDE text editor"

    def registerOptions(self):
        self.options.dynamic.registerOption("fullPlasma", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = None
        if self.options.dynamic.fullPlasma:
            self.runtimeDependencies["kde/frameworks/tier3/plasma-framework"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        if OsUtils.isUnix():
            self.runtimeDependencies["kde/applications/konsole"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if not self.subinfo.options.dynamic.fullPlasma:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_KF5Plasma=ON -DCMAKE_DISABLE_FIND_PACKAGE_KF5ThreadWeaver=ON -DCMAKE_DISABLE_FIND_PACKAGE_KF5NewStuff=ON"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]
        self.defines["icon"] = os.path.join(self.packageDir(), "kate.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "kate", "icons", "128-apps-kate.png")
        self.defines["registy_hook"] = ("""WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate" "" "Edit with Kate"\n"""
                                        """WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate\\command" "" '"$INSTDIR\\bin\\kate.exe" "%V"'\n""")

        self.defines["mimetypes"] = ["text/plain"]
        self.defines["file_types"] = [".ini", ".conf"]


        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return TypePackager.createPackage(self)
