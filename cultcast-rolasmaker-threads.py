from pydub import AudioSegment
import getopt, sys, re, os, tempfile, subprocess, shutil, threading

f = open(sys.argv[1],"r")
urllist = list(f)
f.close()
currentdir = os.getcwd()
rawmp3dir = tempfile.mkdtemp()
#rolas = os.listdir(rawmp3dir)
#os.chdir(currentdir)
introfile = sys.argv[2]
outrofile = sys.argv[3]
intro = AudioSegment.from_mp3(introfile)
outro = AudioSegment.from_mp3(outrofile)

class mixThread(threading.Thread):
    def __init__ (self, i, rawmp3dir, currentdir, intro, url, outro):
        threading.Thread.__init__(self)
        self.pos = i
        self.rawmp3dir = rawmp3dir
        self.currentdir = currentdir
        self.intro = intro
        self.url = url
        self.outro = outro
    def run(self):
        os.chdir(rawmp3dir)
        print 'Descargando '+self.url
        print os.getcwd()
        song = subprocess.check_output(["youtube-dl", "-q", "-s",  "--get-filename", "-x" ,"--audio-format", "mp3", "--audio-quality", "0", self.url])
        subprocess.call(["youtube-dl", "-x" ,"--audio-format", "mp3", "--audio-quality", "0", self.url])
        print song
        mp3song = re.sub(r'\.[^\.]*$', '.mp3', song)
        print os.listdir(self.rawmp3dir)
        print 'Mezclando cortinillas en '+mp3song
        middle = AudioSegment.from_mp3(rawmp3dir+'/'+mp3song)
        prepro = self.intro.append(middle, crossfade=1000)
        output = prepro.append(self.outro, crossfade=1000)
        songfilename = re.sub(r'-............mp3','-Cultcast.mp3', mp3song)
        output.export(self.currentdir+'/'+str("%02d" %  self.pos)+'-'+songfilename, format="mp3")
        print str("%02d" %  self.pos)+'-'+songfilename+' terminada.'

for i, url in enumerate(urllist):
    thread = mixThread(i, rawmp3dir, currentdir, intro, url, outro)
    thread.start()

if thread.isAlive():
    thread.join()

shutil.rmtree(rawmp3dir)
