class i2c_lib :
    def i2ccheckerr(self) :
        f = open('/sys/devices/i2c-0/err', 'r')
        s = f.read(1)
        f.close()
        return int(s)

    def i2csetaddr(self, addr) :
        f = open('/sys/devices/i2c-0/addr', 'w')
        f.write(addr)
        f.close()
        return 0

    def i2csetreg(self, reg) :
        f = open('/sys/devices/i2c-0/reg', 'w')
        f.write(reg)
        f.close()
        return 0

    def i2cgetlock(self) :
        f = open('/sys/devices/i2c-0/lock', 'r')
        s = f.read(1)
        f.close()
        if int(s) == 1 :
            return 1
        return 0

    def i2creleaselock(self) :
        f = open('/sys/devices/i2c-0/lock', 'w')
        f.write('0')
        f.close()
        return 0

    def i2cread(self) :
        if self.i2cgetlock() :
            f = open('/sys/devices/i2c-0/data', 'r')
            s = f.read(8)
            f.close()
            self.i2creleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def i2cwrite(self, arg) :
        if self.i2cgetlock() :
            f = open('/sys/devices/i2c-0/data', 'w')
            f.write(arg)
            f.close()
            self.i2creleaselock()
            return -self.i2ccheckerr()
        else :
            print 'GPIO Busy'
            return -1

    def i2cmultiread(self, num) :
        if self.i2cgetlock() :
            f = open('/sys/devices/i2c-0/numbytes', 'w')
            f.write(num)
            f.close()
            f = open('/sys/devices/i2c-0/wrbytes', 'r')
            ret = f.read(int(num)*5+1)
            f.close()
            self.i2creleaselock()
            return ret.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def i2cmultiwrite(self, num, arg) :
        if self.i2cgetlock() :
            f = open('/sys/devices/i2c-0/numbytes', 'w')
            f.write(num)
            f.close()
            f = open('/sys/devices/i2c-0/wrbytes', 'w')
            f.write(arg)
            f.close()
            self.i2creleaselock()
            return -self.i2ccheckerr()
        else :
            print 'GPIO Busy'
            return -1

    def i2ctest(self, addr) :
        self.i2csetaddr(addr)
        self.i2csetreg(str(0))
        if self.i2cgetlock() :
            f = open('/sys/devices/i2c-0/test', 'r')
            ret = f.read(8)
            f.close()
            self.i2creleaselock()
            return int(ret)
        else :
            print 'GPIO Busy'
            return -1

    def i2cparse(self, addr, reg, rw, data) :
        self.i2csetaddr(addr)
        self.i2csetreg(reg)
        if int(rw) == 0 :
            wordCount = data.count(',')+1
            datalist = data.replace(',', ' ')
            return self.i2cmultiwrite(str(wordCount), datalist)
        else :
            return self.i2cmultiread(rw)
