lname = raw_input("longname: ")
sname = raw_input("shortname: ")
table = ["Immediate", "IMM","Zero Page", "ZPG", "Zero Page X", "ZPX", "Absolute", "ABS",
         "Absolute X", "ABX", "Absolute Y", "ABY", "Indirect X", "IDX", "Indirect Y", "IDY"]
for i in range(0,len(table),2):
    print '        0x : ("%s (%s)",%s"%s %s", self.%s, self.A_%s, None),' % (lname, table[i]," "*(12-len(table[i])),sname,table[i+1],sname, table[i+1])
