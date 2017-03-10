import os, sys, getopt

def Extract(inFile, inSeparator, collums, outFile, outSeparator = ","):
    '''
    extract specified collums from input file, save the result to the output file
    :param inFile: string, input file path which extract from
    :param inSeparator: string, separator of each line in the input file
    :param collums: string, collums extract from the input file, format like "1, 2, 4"
    :param outFile: string, output file path which save the extract result
    :param outFeparator: string, separator of collum item for save result in the output file
    :return:
    '''
    inFile, outFile = open(inFile, 'r'), open(outFile, 'w+')
    collums = collums.split(",")

    for line in inFile:
        inItems = line.strip().split(inSeparator)
        outItems = []

        for collum in collums:
            idx = int(collum)
            if(idx > len(inItems)):
                outItems.append('')
            else:
                outItems.append(inItems[idx])

        if(len(outItems) > 0):
            outFile.write(outSeparator.join(outItems)+"\n")

    inFile.close()
    outFile.close()

def Join(file1, separator1, collum1, file2, separator2, collum2, outFile, outSeparator = ","):
    '''
    join record in file1(with collum separator1) and file2(with collum separator2) on file1.collum1 = file2.collum2,
    save the result to outfile with collum separator
    :param file1: string, first input file path
    :param separator1: string, collum separator of first input file
    :param collum1: int, collum to  join of first file
    :param file2: string, second input file path
    :param separator2: string, collum separator of second input file
    :param collum2: int, collum to  join of second file
    :param outFile: string, path of the output file for save the join result
    :param outSeparator: string, collum separator for output record
    :return:
    '''
    sFile1, sFile2 = file1+".sort", file2+".sort"

    if separator1.isspace():
        os.system("sort -k %d -o %s %s" % (collum1, sFile1, file1))
    else:
        os.system("sort -t %s -k %d -o %s %s" % (separator1, collum1, sFile1, file1))

    if separator2.isspace():
        os.system("sort -k %d -o %s %s" % (collum2, sFile2, file2))
    else:
        os.system("sort -t %s -k %d -o %s %s" % (separator2, collum2, sFile2, file2))

    collum1, collum2 = collum1-1, collum2-1
    items1, items2 = None, None
    sFile1, sFile2, outFile = open(sFile1), open(sFile2), open(outFile, "w")
    for line1 in sFile1:
        items1 = line1.strip().split(separator1)
        if items2 != None:
            if items1[collum1] < items2[collum2]:
                continue #move position of file1 forward
            elif items1[collum1] == items2[collum2]:
                outFile.write(outSeparator.join(items1)+outSeparator+outSeparator.join(items2)+"\n")
                items1, items2 = None, None
                continue #move position of both file forward

        for line2 in sFile2:
            items2 = line2.strip().split(separator2)
            if items1[collum1] == items2[collum2]:
                outFile.write(outSeparator.join(items1)+outSeparator+outSeparator.join(items2)+"\n")
                items1, items2 = None, None
                break #move position of both file forward
            elif items1[collum1] > items2[collum2]:
                continue #move position of file2 forward
            else:
                break #move position of file1 forward

    sFile1.close(), sFile2.close(), outFile.close()


def LeftJoin(file1, separator1, collum1, file2, separator2, collum2, outFile, outSeparator = ","):
    pass

def RightJoin():
    pass

if __name__ == "__main__":
    #Extract("test3", ",", "1, 3", "test4", ",")
    Join("test5", " ", 2, "test6", " ", 2, "test56", "-")