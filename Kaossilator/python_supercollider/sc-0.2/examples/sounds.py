import sc
import time, os


# we need to tell python where the scserver application lives, this
# changes between platforms and systems. You might need to edit it.
# exedir = 'usr/local' # where does scsynth live?
# sc.start(exedir, verbose=1, spew=1 )

sc.start()

player = sc.Synth( "StereoPlayer" )

player.bufnum = sc.loadSnd( "numeros.wav", wait=True )

print "loading bufnum with ID", player.bufnum

time.sleep(5) # wait while sound plays

sc.unloadSnd( player.bufnum )
player.free()
sc.quit()

print 'quiting'

