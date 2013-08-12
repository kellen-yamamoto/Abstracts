class spi_lib :

    def spisetcmd(self, cmd) :
        wordCount = cmd.count(',')+1
        datalist = cmd.replace(',', ' ')
        writestr = str(wordCount)+' '+datalist
        f = open('/sys/bus/spi/devices/spi1.0/cmd', 'w')
        f.write(writestr)
        f.close()
        return 0

    def spisetnumrw(self, num) :
        f = open('/sys/bus/spi/devices/spi1.0/numrw', 'w')
        f.write(num)
        f.close()
        return 0

    def spigetlock(self) :
        f = open('/sys/bus/spi/devices/spi1.0/lock', 'r')
        s = f.read(1)
        f.close()
        if int(s, 0) == 1 :
            return 1
        return 0

    def spireleaselock(self) :
        f = open('/sys/bus/spi/devices/spi1.0/lock', 'w')
        f.write('0')
        f.close()
        return 0

    def spiread(self, length) :
        if self.spigetlock() :
            self.spisetnumrw(length)
            f = open('/sys/bus/spi/devices/spi1.0/data', 'r')
            s = f.read(int(length, 0)*5)
            f.close()
            self.spireleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def spiwrite(self, arg) :
        if self.spigetlock() :
            wordCount = arg.count(',')+1
            datalist = arg.replace(',', ' ')
            self.spisetnumrw(str(wordCount))
            f = open('/sys/bus/spi/devices/spi1.0/data', 'w')
            f.write(datalist)
            f.close()
            self.spireleaselock()
            return 0
        else :
            print 'GPIO Busy'
            return -1

    def spiparse(self, cmd, rw, data) :
        self.spisetcmd(cmd)
        if int(rw, 0) == 0 :
            self.spiwrite(data)
            return 0
        else :
            return self.spiread(rw)
