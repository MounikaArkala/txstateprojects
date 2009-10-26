#TODO: let them type "list" to display a list of professors again.
#TODO: add sys.argv support so they can run it from cmdline if they want to.
#Also, e-mail him about how his e-mail is displayed incorrectly in the document.

baseurl = "http://www.cs.txstate.edu"
faculty_link = baseurl+"/Personnel/Faculty"

import re, urllib2, sys, os
faculty_list = re.compile(r"<h1 id=\"top\">Faculty</h1>(.*?)</td>", re.DOTALL)
faculty = re.compile(r"<li><a href=\"(.*?)\">(.*?)</a><br/>(.*?)</li>", re.DOTALL)

temp = [r'<h1 id="top">(.*?)</h1>', # get their name
        r'<h1 id="top">.*?</h1>.*?<p><em>(.*?)</em>', # position
        r'<h2>Education</h2>.*?<p>(.*?)</p>', # education
        r'<h2>Research\ Interests</h2>.*?<p>(.*?)</p>', #research interests
        r'<h2>E-Mail</h2>.*?<img\ src="/common/email-image.php\?user=(.*?)&domain=(.*?)">',
        r'<h2>Webpage</h2>.*?<a\ href="(.*?)">'] #URL of their website.

info = [re.compile(i, re.DOTALL) for i in temp]



infile = raw_input("Input file (or leave blank for automatic retrieval): ").strip()
outfile = raw_input("Output file (or leave blank for stdout): ").strip()
if infile:
        while not os.path.exists(infile):
            print "--------------------------------------------"
            print "Well... turns out that file '%s' doesn't exist on disk," % infile
            print "so we're just gonna have to ask you for another one!"
            print "(or you can just hit 'enter' if you don't really want an input file.)"
            infile = raw_input("What'll it be? ")
            if infile.strip() == "":
                break
        try:
            text = open(infile, 'r').read() #read in their file.
            
            print "--------------------------------------"
            print "You have chosen to process an input file (%s)." % infile
            print "--------------------------------------"
        except IOError:
            infile = ""


# Show them all the current prof's.
text = urllib2.urlopen(faculty_link).read()
text = re.search(faculty_list, text).groups()[0] # get rid of all that extra crap that causes false results.
print "This is a list of all professors on campus."
to_exit = False
names = {}
for site, name, desc in re.findall(faculty, text):
    lname, fname = name.split(',')
    lname = lname.strip()
    fname = fname.strip()
    print "%s %s (%s)" % (fname, lname, desc)
    names[lname] = names[fname] = (fname+" "+lname, site)
print "-------------------------------"

while 1:
    if not infile:
        matched = []
        while len(matched) != 1:
            matched = []
            name = raw_input("Search: ")
            name = name.strip()
            if name == 'exit':
                to_exit = True
                break
            regexes = []
            for i in name.split(): # in case they have multiple keywords
                regexes.append(re.compile(r".*?%s.*?" % i, re.IGNORECASE))
            for item in names.keys():
                for regex in regexes:
                    if re.search(regex, item): #matches
                        matched.append(names[item])

            #get rid of duplicates in case we matched both first / last name (eg. Lu matches Lucy and Lu so she would be added twice.)
            matched = list(set(matched))
            if len(matched) > 1:
                print "That query matched the following people:"
                for i in matched:
                    print i[0]
                print "Please use a more restrictive query."
            elif len(matched) == 0:
                print "That query found no results."

        if to_exit:
            break


            
        matched = matched[0]
        print "--------------------------------------"
        print "You have chosen to process %s." % matched[0]

        print "--------------------------------------"
    
        text = urllib2.urlopen(baseurl+matched[1]).read()
    
    
    results = []
    for regex in info:
        try:
            result = re.search(regex, text).groups()
            result = "@".join(result) # we shouldn't assume this but we're going to anyway.
        except:
            result = "Unknown"
        results.append(result)
    if outfile:
        backup = sys.stdout
        print "Sending output to disk (%s)." % outfile
        if os.path.exists(outfile):
            decision = ""
            while not decision:
                decision = raw_input("File %s already exists on disk.  Do you want to append or overwrite? " % outfile).strip().lower()
                if decision == 'append':
                    sys.stdout = open(outfile, 'a')
                    print "---------------------------------"
                elif decision == 'overwrite':
                    sys.stdout = open(outfile, 'w')
                else:
                    print "I did not understand your response, please try again!"
                    decision = ""
            
        #just redirect stdout to our new file so we can use the same print statements.
    print 'Name:', results[0]
    print 'Position:', results[1]
    print 'Education:', results[2]
    for index,interest in enumerate(results[3].split(',')):
        interest = interest.strip().lower() #get rid of whitespace and lowercase it.
        print 'Research Interest %s: %s' % (str(index+1), interest.strip())
    print 'Email:', results[4]
    print 'Webpage:', results[5]
    if outfile:
        sys.stdout = backup
        print "File output successful!" # otherwise we'd have gotten an uncaught exception, ruh roh, so we can assume it went okay if we're here.
    print "--------------------------------------"
   
    if infile:
        print "Input file done processing, exiting."
        break # no point in looping on a non-changing input file.
        
    print "Hint: if you are finished, type 'exit'."