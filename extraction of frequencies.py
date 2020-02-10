import numpy, wave, struct
sampling_freq = 0.0
file_length = 0.0
total_time = 0.0
window_time = 2.15 # Set time slice for window "Can be adjustable in different scenario"
window = 0.0 # Declaration of global varible window size
number_of_windows = 0 #Declaration of global varible number of windows
# Indexing info:
last_index = 0
prev_freq_in_hertz = 0.0
# Threshold and frequency adjustments info:
freq_adjust =40 # Frequency adjustment threshold (-10Hz ~ +10) "Can be adjustable in different scenario"
# Note identification function:
def identify_notes(frequency_data):
        notes_array = ['C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6','F4',
                 'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7','B3',
                 'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8',
                 'A4','E4','G3','C3','A3','A5','F4']
        frequency_array = [1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,349.00,
                 2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,246.00,
                 4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13,
                 440.00,329.63,196.00,130.81,220.00,880.00,329.63]

        final_note = ""
        if frequency_data > 0:
                for note in range(len(notes_array)):
                        if frequency_data == frequency_array[note] or frequency_array[note]-freq_adjust <= frequency_data <= frequency_array[note]+freq_adjust:
                                final_note = notes_array[note]
                                break
                        #else:
                                #final_note = "NULL"
        return final_note
# RMS check function:
def check_window(window_data):
        global last_index
        k = 0
        check_frame = numpy.zeros(window,dtype=numpy.int)
        check_frame = numpy.array(check_frame)
        if last_index < (file_length - window):
                for k in range(window):
                        check_frame[k]=window_data[k+last_index]
                last_index += window+1


        return check_frame
# Peak frequency check function:
def peak_freq(raw_data):
        dft = numpy.fft.fft(raw_data)
        dft=numpy.argsort(dft)
        if(dft[0]>dft[-1] and dft[1]>dft[-1]):
            i_max = dft[-1]
        elif(dft[1]>dft[0] and dft[-1]>dft[0]):
            i_max = dft[0]
        else :
            i_max = dft[1]
        freq_in_hertz = (i_max * sampling_freq)/94815
        print(freq_in_hertz)
        return (freq_in_hertz)
# Main play function:
def play(sound_file):
        global sampling_freq, audio_channel, file_length, total_time, window, check_frame, number_of_windows, prev_freq_in_hertz
        #print("Reading file: " + str(file_name) + " ...")

        sampling_freq = sound_file.getframerate() # Get sampling freq. or frame rate
        file_length = sound_file.getnframes() # Get number of frames
        total_time = file_length/float(sampling_freq) # Calculate total time of all samples in seconds
        window = 94815# Calculate length of window (0.05 Sec * 44100 Hz = 2205)
        number_of_windows = (file_length / window) # Calculate number of windows
        data = sound_file.readframes(file_length) # Read and assign 2byte data from crrent frame to a new array "data"
        sound_file.close() # Close the file after reading the stream
        data = struct.unpack('{n}h'.format(n=file_length), data) # Unpack 2byte data one-by-one and assign again to "data" array
        data = numpy.array(data) # Reformat data to array
        final_note_array = []
        count=0
        a=0
        b=0
        for g in range(number_of_windows):
                check_frame = check_window(data)
                freq_in_hertz = peak_freq(check_frame)
                a=count
                #print(a,b)
                if freq_in_hertz != prev_freq_in_hertz and freq_in_hertz !=0:
                        final_note = identify_notes(freq_in_hertz)
                        count=count+1
                        b=count
                        if final_note != "NULL":
                                final_note_array.append(final_note)

                else:
                    count=count+1
                prev_freq_in_hertz = freq_in_hertz
                #print(a,b)
                if a==b:
                    #print ('onset',a-1)
                    print(identify_notes(freq_in_hertz))
                    print(freq_in_hertz)
        final_note_array = numpy.array(final_note_array)
        result = ""
        for notes in range(len(final_note_array)):
                result += " " + str(final_note_array[notes])
        Inentified_Notes = result
        return Inentified_Notes
# Script main thread:
if __name__ == "__main__":
    Identified_Notes_list = []
    for file_number in range(1,2 ):
        file_name = "Test_Audio_files\Audio_" + str(file_number)+".wav"
        sound_file = wave.open('C:\\Users\\Ritvik\\Desktop\\Audio_1.wav','r')
        Identified_Notes = play(sound_file)
        Identified_Notes_list.append("Identifed notes(File: " + file_name + "):" + Identified_Notes)
    for Identified_Notes in Identified_Notes_list:
        print Identified_Notes
