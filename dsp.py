import numpy as np

def sign(num):
    if num >= 0:
        return True
    if num < 0:
        return False

def signalIsolate(samples, sampleRate, threshold):
    dataStart = np.where(samples > threshold)[0][0]
    dataEnd = len(samples)-1
    counter = 0
    for i in range(dataStart, len(samples)):
        if samples[i] < threshold :
            counter+=1
        else :
            counter = 0
        if counter > round(sampleRate/100):
            dataEnd = round(i-sampleRate/100)
            break
    return samples[dataStart:dataEnd], dataStart, dataEnd

def findTimings(samples):
    if len(samples) == 0:
        return 0,0,0
    lastVal = samples[0]
    highestVal = 0
    zeros = [0]
    peaks = []
    timings = []
    #FIND ZERO CROSSINGS AND PEAKS
    for i, sample in enumerate(samples):
        if abs(sample) > abs(samples[highestVal]):
            highestVal = i
        if sign(sample) != sign(lastVal):
            zeros.append(i)
            peaks.append(highestVal)
            lastVal = sample
            highestVal = i
    #FIND PEAK TIMINGS
    for i in range(1, len(peaks)):
        timings.append(peaks[i] - peaks[i-1])
    return zeros, peaks, timings

def boundsDecode(timings, ignore, tolerance):
    if len(timings) == 0 or len(timings) < ignore*2:
        return 0,0,0,0
    lowerBound = np.zeros(len(timings))
    lowestVal = 0
    for i in range(0, ignore, 1):
        lowestVal += timings[i]
    lowestVal /= ignore
    higherBound = np.zeros(len(timings))
    highestVal = 0
    for i in range(-1, -(ignore+1), -1):
        highestVal += timings[i]
    highestVal /= ignore
    averageBound = np.zeros(len(timings))
    bits = ""
    for i in range(ignore, len(timings), 1):
        if timings[i] < lowestVal and tolerance > lowestVal/timings[i]:
            lowestVal = timings[i]
        lowerBound[i] = lowestVal
    for i in range(0, ignore):
        lowerBound[i] = lowerBound[ignore]
    for i in range(len(timings)-1-ignore, -1, -1):
        if timings[i] > highestVal and tolerance > timings[i]/highestVal:
            highestVal = timings[i]
        higherBound[i] = highestVal
    for i in range(len(timings)-1, len(timings)-1-ignore, -1):
        higherBound[i] = higherBound[-(ignore+1)]
    for i in range(len(timings)):
        averageBound[i] = (lowerBound[i]+higherBound[i])/2
        
    count = 0
    while count < len(timings)-1:
        if timings[count] > averageBound[count]:
            bits+="0"
        if timings[count] < averageBound[count] and timings[count+1] < averageBound[count]:
            bits+="1"
            count+=1
        count += 1
    return lowerBound, higherBound, averageBound, bits