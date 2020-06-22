import wave, struct, math, random
from flask import Flask, escape, request, render_template, jsonify, send_file
import threading
import time
import os
import wave
OCTAVE = 12
MAXAMP=32767.0

class Scale:
	def __init__(self, scale):
		self.scale=scale

class Note:
	def __init__(self, tempo, sampleRate ,duration, chord, volume=1,stime=0.1):
		self.tempo=tempo
		self.sampleRate=sampleRate
		self.duration=duration
		self.chord=chord
		self.volume=volume
		self.stime=stime

file='h.wav'
app = Flask(__name__)
length=300
form=[]
files=open("static/files.txt", 'r').read().split('\n')
i=0
noteToFreq = {}
freqToNote= {}
freq=[]
scales={}
def readFreqs():
	reader = open("static/note_frequencies.txt", 'r')
	line = reader.readline()
	while line != '':
	    noteToFreq[line.split()[0]] = float(line.split()[1])
	    freqToNote[float(line.split()[1])] = line.split()[0]
	    freq.append(float(line.split()[1]))
	    line = reader.readline()
	reader.close()

def writeNotes(notes, wavef):
	for note in notes:
		writeChord(note.tempo,note.duration,note.sampleRate,note.chord,note.volume,wavef,note.stime)

def writeChord(tempo, l, rate, chord, volume, f, stime):
    value = 0
    amplitude = 20000.0
    pos_a = 0
    if l!=0:
        pos_a = amplitude/((10 / tempo) * l * rate)
        neg_a = amplitude / (((50 / tempo) * l * rate))
    for i in range(int((60 / tempo) * l * rate)):
        a = i * pos_a
        if (a >= amplitude):
            a = amplitude - (i-((10 / tempo) * l * rate))*neg_a
        value = 0
        for k in chord:
            value += (math.sin(noteToFreq[k] * math.pi * float(i) / float(rate)))
        value = int(a * (value / len(chord)))
        # print(value)
        data = struct.pack('<h', value)
        f.writeframesraw(data)
    # dv = max(3 * (32767.0 - value) / int(stime * rate), 0)
    # for i in range(int(stime * rate)):
    #     f.writeframesraw(struct.pack('<h', int(min(value + i * dv, 32767.0))))


def getlength(b):
    c = 0
    for i in b:
        c += i
        c += .1
    return c


def getInput(fileName):
	reader = open("input.txt", 'r')
	sampleRate = int(reader.readline())
	tempo = int(reader.readline())
	notes=[]
	line = reader.readline()
	while line != '':
	    notes.append(Note(tempo,sampleRate,float(line.split()[1]),line.split()[0].split(",")))
	    line = reader.readline()
	return [sampleRate,tempo,notes]

def openFile(fileName,sampleRate):
	wavef = wave.open(fileName, 'w')
	wavef.setnchannels(1)  # mono
	wavef.setsampwidth(2)
	wavef.setframerate(sampleRate)
	return wavef

def closeFile(wavef,sampleRate):
	dv = (MAXAMP) / int(.1 * sampleRate)
	for i in range(int(.1 * sampleRate)):
	    wavef.writeframesraw(struct.pack('<h', 0))
	wavef.writeframes(struct.pack('<h', 0))
	wavef.close()

def writefromInput(args):
	sampleRate,tempo, notes=getInput(args.input)
	wavef=openFile(args.output,sampleRate)
	writeNotes(notes, wavef)
	closeFile(wavef,sampleRate)



def createScales():
 	scales["C Major"]=[noteToFreq['C5'],noteToFreq['D5'],noteToFreq['E5'],noteToFreq['F5'],noteToFreq['G5'],noteToFreq['A5'],noteToFreq['B5']]


def readMusic(file='h.wav'):
	global form
	wavef = wave.open("static/"+file,'rb')
	f = (list(map(lambda x:int(x/5),wavef.readframes(wavef.getnframes()))))
	x=0
	d=[]
	form=[]
	comp=int(wavef.getframerate()/100)
	for j in range(len(f)):
		if ((j+1)%16 !=0):
			x+=f[j]
		else:
			d.append(int(x/(16)))
			x=0

	for j in range(len(d)):
		if ((j+1)%comp ==0):
			form.append(d[j])
	wavef.close()

def writeNote(tempo, len, rate, freq, f, stime=0.1):
    value = 0
    for i in range(int(60 / tempo * (len) * rate)):
        value = int(32767.0 * math.cos(freq * math.pi * float(i) / float(rate)))
        data = struct.pack('<h', value)
        f.writeframesraw(data)
    dv = (32767.0 - value) / int(stime * rate)
    for i in range(int(stime * rate)):
        f.writeframesraw(struct.pack('<h', int(value + (i * dv))))


def writeNotes(tempo, l, rate, freqs, f, stime=0.1):
    value = 0
    for i in range(int((int(60 / tempo * (l) * rate)))):
        value = 0
        for k in freqs:
            value += (math.cos(Notes[k] * math.pi * float(i) / float(rate)))
        value = int(32767.0 * (value / len(freqs)))
        # print(value)
        data = struct.pack('<h', value)
        f.writeframesraw(data)
    dv = (32767.0 - value) / int(stime * rate)
    for i in range(int(stime * rate)):
        f.writeframesraw(struct.pack('<h', int(value + (i * dv))))

def randMusic(str):
    tempo = 120
    sampleRate = 44100.0
    c = {2: noteToFreq["C5"], 3: noteToFreq["D5"], 5: noteToFreq["E5"], 1: noteToFreq["F5"], 6: noteToFreq["G5"], 7: noteToFreq["A5"], 4: noteToFreq["B5"]}
    wavef = wave.open('static/'+ str, 'w')
    wavef.setnchannels(1)  # mono
    wavef.setsampwidth(2)
    wavef.setframerate(sampleRate)
    # line = reader.readline()
    # while line != '':
    #     writeNotes(tempo, int(line.split()[1]), sampleRate, line.split()[0].split(","), wavef)
    #     line = reader.readline()
    for i in range(random.randint(5, 30)):
        writeChord(tempo, random.randint(1, 4), sampleRate, c[random.randint(1, 7)], wavef)
    dv = (32767.0) / int(0.1 * sampleRate)
    for i in range(int(0.1 * sampleRate)):
        wavef.writeframesraw(struct.pack('<h', int(32767 - (i * dv))))
    writeNote(tempo, 1, sampleRate, c[1], wavef)
    wavef.writeframes(struct.pack('<h', 0))
    wavef.close()

file=files[-1]
@app.route('/')
@app.route('/home')
def home(f=file):
	global i
	global form
	readFreqs()
	readMusic(f)
	#print(file)
	return render_template('wave.html', length = min(length,len(form[i:])),form=form[i:], file = f)

@app.route('/playWave', methods=['POST'])
def update():
	global i
	i+=1
	return render_template('layout_1.html', length = length,form=form[i:])

@app.route('/check', methods=['POST'])
def check():
	global i
	return jsonify({'length': len(form[i:])-(length + 1)})

@app.route('/resetWave', methods=['POST'])
def reset():
	global i
	i=0
	return render_template('layout_1.html', length = length,form=form[i:])

@app.route('/updateFile', methods=['POST'])
def fileUpdate():
	if request.get_json()['file'] not in files:
		files.append(request.get_json()['file'])
	writer=open("static/files.txt", 'w')
	for filename in files:
		if (filename != ''):
			writer.write(filename+"\n")		
	writer.close()
	randMusic(files[-1])
	file=files[-1]
	global i
	i=0
	return home(request.get_json()['file'])

@app.route('/download')
def downloadFile ():
    path = os.path.join(os.path.dirname(__file__),'static',file)
    return send_file(path, as_attachment=True)

if __name__ =="__main__":
	app.run(debug=True)
	