

temp = [all_notes[i] for i in series.split()]
print '<div id="occurrence">Occurrences of <table class="primesresult">' + pretty(temp, encoding) + "</table><br />"
result = detect(rownumerals, temp)
if len(result) == 0:
    print "No occurrences were found!<br />"
for item in detect(rownumerals, temp):
    markupstr = '<table class="primesresult"><tr>%s</tr></table>'
    datastr = ""
    for i in range(12):
        if i >= item[2] and i < (item[2] + len(series.split())):
            datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
        else:
            datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
    print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)

print "</div>"
	