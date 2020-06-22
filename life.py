import wave, struct, math, argparse
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

noteToFreq = {}
freqToNote= {}
freq=[]
scales={}
def readFreqs():
	reader = open("note_frequencies.txt", 'r')
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

def main():
	parser=argparse.ArgumentParser()
	parser.add_argument("-i","--input",
                        help='Used to specify input file',
                        default="input.txt",
                        type=str)
	parser.add_argument("-o","--output",
                        help='Used to specify output file',
                        default="sound.wav",
                        type=str)
	args=parser.parse_args()
	readFreqs()
	# writefromInput(args)



if __name__ == '__main__':
	main()
	