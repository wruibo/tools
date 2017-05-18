'''
    file tools
'''
import os


class File:
    def __init__(self, file):
        self.file = file

    @staticmethod
    def open(path, mode, buffering=-1):
        file = open(path, mode, buffering)
        if not file:
            return None

        return File(file)

    def head(self, lines=1):
        '''
            read @lines head lines
        :param lines:
        :return:
        '''
        #move to file head
        self.file.seek(0, 0)

        #read lines
        rlines = []
        line = self.file.readline()
        while lines > 0 and line:
            rlines.append(line)
            line = self.file.readline()
            lines -= 1

        return None if len(rlines)==0 else rlines

    def tail(self, lines=1):
        '''
            read @lines tail lines
        :param lines:
        :return:
        '''
        #get the file size
        fsize = self.file.tell()

        #read step size in bytes
        rpos, stepsz = 0, 256
        rpos += stepsz
        rpos = rpos if fsize > rpos else fsize

        #move to the end of file
        self.file.seek(-rpos, 2)
        rlines = self.file.readlines()
        while len(rlines) < lines and rpos < fsize:
            rpos += stepsz
            rpos = rpos if fsize > rpos else fsize

            rlines = self.file.readlines()

        return None if len(rlines)==0 else rlines[-lines:]

    def first_line(self):
        '''
            read first line
        :return:
        '''
        lines = self.head(1)
        return None if lines is None else lines[0]

    def last_line(self):
        '''
            read the last line
        :return:
        '''
        lines = self.tail(1)
        return None if lines is None else lines[-1]


if __name__ == "__main__":
    file = File.open("cini.py", 'r')
    print "first line: %s" % file.head(3)
    print "last line: %s" % file.tail(1)