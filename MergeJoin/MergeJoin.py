ans = []
currentId = ''
buffer = []
maxBufferLength = 0
with open("R_sorted.tsv") as fr:
    with open("S_sorted.tsv") as fs:
        lineR = fr.readline()
        lineS = fs.readline()
        while lineR != "":
            lineR = lineR.strip('\n')
            listR = lineR.split('\t')
            lineRId = listR[0]
            lineS = lineS.strip('\n')
            listS = lineS.split('\t')
            lineSId = listS[0]
            if lineRId == currentId and lineRId != lineSId:
                ans.append(
                    [currentId] + listR[1:] + buffer)
                lineR = fr.readline()
            elif lineRId == lineSId:
                if lineRId != currentId:
                    buffer = []
                    currentId = lineRId
                buffer.extend(listS[1:])
                lineS = fs.readline()
            elif lineRId < lineSId:
                if lineRId != currentId:
                    if len(buffer) > maxBufferLength:
                        maxBufferLength = len(buffer)
                    buffer = []
                lineR = fr.readline()
            elif lineRId > lineSId:
                if len(buffer) > maxBufferLength:
                    maxBufferLength = len(buffer)
                buffer = []
                lineS = fs.readline()

with open("RSMergeJoin.tsv", "w") as fj:
    fj.write("Max Buffer Size: " + str(maxBufferLength) + '\n\n')
    for i in ans:
        fj.write('\t'.join(i) + '\n')
        print(i)
    print("Max Buffer Size: " + str(maxBufferLength))
