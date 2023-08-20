with open("../data/inputs/R_sorted.tsv") as fr:
    with open("../data/inputs/S_sorted.tsv") as fs:
        with open("../data/outputs/RSUnion.tsv", "w") as fj:
            lineR = fr.readline()
            lineS = fs.readline()
            while lineR != "" or lineS != "":
                lineR = lineR.strip("\n")
                listR = lineR.split("\t")
                lineRId = listR[0]
                lineS = lineS.strip("\n")
                listS = lineS.split("\t")
                lineSId = listS[0]
                if lineR == "":
                    fj.write(lineS + "\n")
                    lineS = fs.readline()
                elif lineS == "":
                    fj.write(lineR + "\n")
                    lineR = fr.readline()
                else:
                    if lineRId == lineSId:
                        if listR[1:] != listS[1:]:
                            fj.write(lineR + "\n")
                            fj.write(lineS + "\n")
                        else:
                            fj.write(lineR + "\n")
                        lineR = fr.readline()
                        lineS = fs.readline()
                    elif lineRId < lineSId:
                        fj.write(lineR + "\n")
                        lineR = fr.readline()
                    elif lineRId > lineSId:
                        fj.write(lineS + "\n")
                        lineS = fs.readline()
