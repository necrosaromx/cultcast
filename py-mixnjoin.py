import getopt, sys
from pydub import AudioSegment


try:
    opts, args = getopt.getopt(sys.argv[1:],"mj1:2:p:o:")
except getopt.GetoptError:
    print sys.argv[0] + ' -m|-j [m to mix, j to join] -1 File1 -2 File2 -p position(ms) or delay -o outputfile'
    sys.exit(2)
#logging.debug('Argumentos %s', args)
for opt, arg in opts:
    if opt == "-m":
        action = "mix"
    elif opt == "-j":
        action = "join"
    elif opt == "-1":
        file1 = arg
    elif opt == "-2":
        file2 = arg
    elif opt == "-p":   
        pos = arg
    elif opt == "-o":
        outfile = arg
    
sound1 = AudioSegment.from_mp3(file1)
sound2 = AudioSegment.from_mp3(file2)

# mix sound2 with sound1, starting at 5000ms into sound1)
if action == "mix":
        output = sound1.overlay(sound2, position=int(pos))
elif action == "join":
        output = sound1.append(sound2, crossfade=int(pos))

# save the result
output.export(outfile, format="mp3")
