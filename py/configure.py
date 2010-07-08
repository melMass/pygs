import os
import shutil
import sipconfig
from PyQt4 import pyqtconfig

config = pyqtconfig.Configuration()

# The name of the SIP build file generated by SIP and used by the build
# system.
build_file = "libpygs.sbf"
sip_files_dir = "sip"
output_dir = "build"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Build the QxtGlobalShortcut library.
os.system("cd lib && qmake && make")

if os.name == 'nt':
    shutil.copyfile(os.path.abspath("lib/release/libpygs.a"),
                    os.path.abspath("lib/libpygs.a"))
    shutil.copyfile(os.path.abspath("lib/release/pygs.dll"), 
                    os.path.abspath("lib/pygs.dll"))
    installs = []
    installs.append([os.path.abspath("lib/release/pygs.dll"), 
                     config.sip_mod_dir])
else:
    installs = []

# Run SIP to generate the code.
command = " ".join(
    [config.sip_bin, "-c", output_dir, "-b", os.path.join(output_dir, build_file),
     "-I"+config.pyqt_sip_dir,
     "-I"+config.qt_inc_dir,
     "-I"+sip_files_dir,
     config.pyqt_sip_flags,
     os.path.join(sip_files_dir, "pygsmod.sip")]
    )

os.system(command)

# Create the Makefile.
makefile = pyqtconfig.QtGuiModuleMakefile(
    config, build_file, dir=output_dir, installs=installs)

makefile.extra_include_dirs.append(os.path.abspath("../libqxt/src/core"))
makefile.extra_include_dirs.append(os.path.abspath("../libqxt/src/gui"))
makefile.extra_lib_dirs.append(sip_files_dir)
makefile.extra_lib_dirs.append(os.path.abspath("lib"))
makefile.extra_libs.append("pygs")

# Generate the Makefile itself.
config.pyqt_modules = config.pyqt_modules.split()
makefile.generate()

del config.pyqt_modules

sipconfig.ParentMakefile(
    configuration = config,
    subdirs = [output_dir]
    ).generate()
