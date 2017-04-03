from pydub import AudioSegment
import getopt, sys, re, os, tempfile, subprocess, shutil
currentdir = os.getcwd()
rawmp3dir = tempfile.mkdtemp()
os.chdir(rawmp3dir)
urllist = sys.argv[1]
subprocess.call(["youtube-dl","--batch-file", urllist, "-x" ,"--audio-format", "mp3", "--audio-quality", "0"])
rolas = os.listdir(rawmp3dir)
os.chdir(currentdir)
introfile = sys.argv[2]
outrofile = sys.argv[3]
intro = AudioSegment.from_mp3(introfile)
outro = AudioSegment.from_mp3(outrofile)

for song in rolas:
    middle = AudioSegment.from_mp3(rawmp3dir+'/'+song)
    prepro = intro.append(middle, crossfade=1000)
    output = prepro.append(outro, crossfade=1000)
    songfilename = re.sub(r'-............mp3','-Cultcast.mp3', song)
    output.export(currentdir+'/'+songfilename, format="mp3")



shutil.rmtree(rawmp3dir)
    
#
## mix sound2 with sound1, starting at 5000ms into sound1)
#if action == "mix":
#        output = sound1.overlay(sound2, position=int(pos))
#elif action == "join":
#
## save the result
#output.export(outfile, format="mp3")
