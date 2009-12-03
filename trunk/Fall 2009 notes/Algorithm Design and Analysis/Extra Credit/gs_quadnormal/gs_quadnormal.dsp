# Microsoft Developer Studio Project File - Name="gs_quadnormal" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Console Application" 0x0103

CFG=gs_quadnormal - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "gs_quadnormal.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "gs_quadnormal.mak" CFG="gs_quadnormal - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "gs_quadnormal - Win32 Release" (based on "Win32 (x86) Console Application")
!MESSAGE "gs_quadnormal - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
RSC=rc.exe

!IF  "$(CFG)" == "gs_quadnormal - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD CPP /nologo /W3 /GX /O2 /I "../../glew/include" /D "GLEW_STATIC" /I "$(CG_INC_PATH)" /I "c:\Program Files\NVIDIA Corporation\Cg\include" /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /c
# ADD BASE RSC /l 0x409 /d "NDEBUG"
# ADD RSC /l 0x409 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib glew.lib cg.lib cgGL.lib  /nologo /subsystem:console /machine:I386
# ADD LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib glew.lib cg.lib cgGL.lib  /nologo /subsystem:console /machine:I386 /libpath:"../../glew/Release;$(CG_LIB_PATH);c:\Program Files\NVIDIA Corporation\Cg\lib"

!ELSEIF  "$(CFG)" == "gs_quadnormal - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Ignore_Export_Lib 0
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD CPP /nologo /W3 /Gm /GX /ZI /Od /I "../../glew/include" /D "GLEW_STATIC" /I "$(CG_INC_PATH)" /I "c:\Program Files\NVIDIA Corporation\Cg\include" /D "WIN32" /D "_DEBUG" /D "_CONSOLE" /D "_MBCS" /YX /FD /GZ /c
# ADD BASE RSC /l 0x409 /d "_DEBUG"
# ADD RSC /l 0x409 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib glew.lib cg.lib cgGL.lib  /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept
# ADD LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib glew.lib cg.lib cgGL.lib  /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept /libpath:"../../glew/Debug;$(CG_LIB_PATH);c:\Program Files\NVIDIA Corporation\Cg\lib"

!ENDIF 

# Begin Target

# Name "gs_quadnormal - Win32 Release"
# Name "gs_quadnormal - Win32 Debug"
# Begin Group "Source Files"
# PROP Default_Filter "cpp;c;h"
# Begin Source File
SOURCE=fast_teapot.c
# End Source File
# Begin Source File
SOURCE=fast_teapot.h
# End Source File
# Begin Source File
SOURCE=gs_quadnormal.c
# End Source File
# Begin Source File
SOURCE=request_vsync.h
# End Source File
# End Group
# Begin Group "Cg Files"
	# PROP Default_Filter "cg;cgfx"
# Begin Source File
SOURCE=gs_quadnormal.cgfx
# End Source File
# End Group

# End Group
# End Target
# End Project
