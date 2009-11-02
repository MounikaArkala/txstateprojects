#
#   	Copyright (c) thanos vassilakis 2000,2001, 2002
#
#	This library is free software; you can redistribute it and/or 
#	modify it under the terms of the GNU Lesser General Public License 
#	as published by the Free Software Foundation; either version 2.1 of the 
#	License, or (at your option) any later version.
#
#	This library is distributed in the hope that it will be useful, but 
#	WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
#	or FITNESS FOR A PARTICULAR PURPOSE.  
#	See the GNU Lesser General Public License for more details.
#
#	See terms of license at gnu.org. 
#
#	$Id: validation.py,v 1.1 2003/01/24 17:33:24 thanos Exp $
__version__="$Revision: 1.1 $"





import traceback
def isZipCode(zipCode):
    try:
        sz = len(zipCode)
        if sz == 10:
            zipCode.index('-',5)
            int(zipCode[:5])
            int(zipCode[6:])
        elif sz in (5, 9):
            code = int(zipCode)
        else:
            raise Exception()
    except:
            raise Exception('Invalid zip code, must be 5 or 9 digits')
    return zipCode

def test(funcwhat, res1, res2, show=0):
    print "trying ", funcwhat, 
    try:
       exec(funcwhat)
    except:
        if show:
            traceback.print_exc()
        print res2
    else:
        print res1
    
if __name__ =='__main__':
    test( "isZipCode('12345-6789')", "OK", "failed")
    test( "isZipCode('123456789')", "OK", "failed")
    test( "isZipCode('12345')", "OK", "failed")
    test( "isZipCode('12345678')", "OK", "failed")
    test( "isZipCode('1234256789AB')", "OK", "failed")
 

