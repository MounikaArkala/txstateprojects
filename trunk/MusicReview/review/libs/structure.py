def print_header(title="Music Analysis", css=[], scripts=[], onload=None):
    css_txt = "".join([('<link rel="stylesheet" type="text/css" href="stylesheets/%s" />\n' % s) for s in css])
    script_txt = "".join([('<script src="scripts/%s"></script>\n' % s) for s in scripts])
    subs = {}
    subs['title'] = title
    subs['scriptlinks'] = css_txt + script_txt
    if onload:
        subs['onload'] = onload
    else:
        subs['onload'] = ""
        
    print "Content-type: text/html"
    print
    print (open("main/header.html").read() % subs)
    
def print_footer():
    print open("main/footer.html").read()


def print_body(filename, subdict=None):
    if subdict:
        temp = open(filename).read()
        print temp % subdict
    else:
        print open(filename).read()
