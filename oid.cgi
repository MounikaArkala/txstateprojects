

notes = [all_notes[i] for i in series.split()]
someresult = False
for perm in all_perms(notes):
	result = detect(rownumerals, perm)
	if len(result) > 0:
		someresult = True
		print '<div id="occurrence">Occurrences of <table class="primesresult">' + pretty(perm, encoding) + "</table><br />"
		for item in result:
			markupstr = '<table class="primesresult"><tr>%s</tr></table>'
			datastr = ""
			for i in range(12):
				if i >= item[2] and i < (item[2] + len(series.split())):
					datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
				else:
					datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
			print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)
		print "</div>"

if not someresult:
    print "That sequence did not occur in any order!<br />"
print "<br /><br />"
	