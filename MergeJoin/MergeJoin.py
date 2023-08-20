currentId = ""
buffer = []
maxBufferLength = 0
with open("../data/inputs/R_sorted.tsv") as fr:
    with open("../data/inputs/S_sorted.tsv") as fs:
        with open("../data/outputs/RSMergeJoin.tsv", "w") as fj:
            lineR = fr.readline()
            lineS = fs.readline()
            while lineR != "":
                lineR = lineR.strip("\n")
                listR = lineR.split("\t")
                lineRId = listR[0]
                lineS = lineS.strip("\n")
                listS = lineS.split("\t")
                lineSId = listS[0]
                if lineRId == currentId and lineRId != lineSId:
                    fj.write("\t".join([currentId] + listR[1:] + buffer) + "\n")
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
            fj.write("\nMax Buffer Size: " + str(maxBufferLength) + "\n")
