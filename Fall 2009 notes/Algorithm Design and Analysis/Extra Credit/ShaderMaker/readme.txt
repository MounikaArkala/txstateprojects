

 Shader Maker - a simple, cross-platform GLSL editor
====================================================

This document tells you how to compile the source code, generate the HTML documentation
and run the application.

To install this software, simply unpack it into a directory of your choice. This
software neither registers itself on the system nor creates any config files.
So you can simply delete it if you want to uninstall it.


Compilation:
------------

Prerequisite for compiling the source code: Qt 4.2 or higher, including headers and libraries.
Under Mac OS X: you need also the WebServices package, which is not installed by default with all
the other developer stuff.
(Another library, GLee, which is used by this software, is already included in the source code directory.) 

Compiling the code under Windows:
use the Visual Studio project files located in the subdirectory src/win32/. Open the .sln file, choose
the configuration 'Release', and compile the project.

Compiling under Linux / Mac OS X:
use the .pro file located in the root directory.
The following command sequence should work on Linux and MacOS:

$ cd /path/to/glsleditor/src
$ qmake-qt4
$ make

If you have only Qt4 installed, then 'qmake' suffices.
(However, with current Linux distros, there is often also Qt3 pre-installed.)

To clean up temporary files, you can type

$ make clean

Compiling under Mac OS X:
use either the same procedure as for Linux, or use the XCode 3.0 project.

If you need to re-generate the XCode project files, simply do
$ qmake -spec macx-xcode shadermaker.pro



Running the program:
--------------------

To run the compiled application, run shadermaker in the root directory:

$ cd /path/to/glsleditor/
$ ./shadermaker

Windows users run ShaderMaker.exe in the same directory.

Documentation:
--------------

If you want to build the documentation, you need Doxygen 1.5.4 or higher.
Then, on the command line, cd into the doc/ directory. Then run doxygen:

$ cd /path/to/glsleditor/doc/
$ doxygen

Afterwards, the HTML documentation can be found in doc/html/ .


Known issues:
-------------

- On Mac OS the options 'Switch to SDI view' and 'Switch to MDI view' freeze the program.
  The reason is unknown, because the feature workes well on Windows and Linux, but it seems
  that a bug in Qt is responsible. If you encounter this problem, you can hard-code your
  preferred view by editing the method CEditor::init() in editor.cpp.

- On Mac OS and Windows XP there is a problem with button colors.
  Several buttons in the GUI bring up a color selection dialog when clicked.
  The selected color is then used as the button's background color.
  Unfortunately, this does not work on some platforms. The buttons are drawn
  with the system's default colors. This appears on Mac OS and Windows XP. On Windows XP,
  this problem appears only when using the default theme. When switching to the 'classic'
  theme, the buttons are drawn correctly. The behaviour on Windows Vista is unknown and not tested.
  The reasons is unknown, but seems to be a bug in Qt or in the underlying operating system.
  A possible workaround whould be to use a built-in style of Qt, where Qt draws everything by itself.



