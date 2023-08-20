rList = []
currentId = ""
buffSumm = 0
with open("../data/inputs/R.tsv") as fr:
    with open("../data/outputs/RSumGroupBy.tsv", "w") as fj:
        for line in fr:
            rList.append(line.strip("\n").split("\t"))
        rList.sort(key=lambda x: x[0])
        for r in rList:
            if r[0] == currentId:
                buffSumm += int(r[1])
            else:
                if currentId != "":
                    fj.write(currentId + "\t" + str(buffSumm) + "\n")
                currentId = r[0]
                buffSumm = int(r[1])
