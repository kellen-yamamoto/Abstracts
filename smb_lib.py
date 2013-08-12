class smb_lib :

    def smbcheckerr(self) :
        f = open('/sys/devices/i2c-0/err', 'r')
        s = f.read(1)
        print s
        f.close()
        return int(s)

    def smbsetaddr(self, addr) :
        f = open('/sys/devices/i2c-0/addr', 'w')
        f.write(addr)
        f.close()
        return 0

    def smbsetcmd(self, reg) :
        f = open('/sys/devices/i2c-0/reg', 'w')
        f.write(reg)
        f.close()
        return 0

    def smbgetlock(self) :
        f = open('/sys/devices/i2c-0/lock', 'r')
        s = f.read(1)
        f.close()
        if int(s) == 1 :
            return 1
        return 0

    def smbreleaselock(self) :
        f = open('/sys/devices/i2c-0/lock', 'w')
        f.write('0')
        f.close()
        return 0

    def smbsetnumbytes(self, num) :
        f = open('/sys/devices/i2c-0/numbytes', 'w')
        f.write(num)
        f.close()
        return 0

    def smbsetextcmd(self, cmd) :
        f = open('/sys/devices/i2c-0/extcmd', 'w')
        f.write(num)
        f.close()
        return 0

    def smbreadbytes(self, length) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/wrbytes', 'r')
            s = f.read(int(length)*5+1)
            f.close()
            self.smbreleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def smbwritebytes(self, arg) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/wrbytes', 'w')
            f.write(arg)
            f.close()
            self.smbreleaselock()
            return -self.smbcheckerr()
        else :
            print 'GPIO Busy'
            return -1

    def smbrecievebytes(self, length) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/srbytes', 'r')
            s = f.read(int(length)*5+1)
            f.close()
            self.smbreleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def smbsendbytes(self, arg) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/srbytes', 'w')
            f.write(arg)
            f.close()
            self.smbreleaselock()
            return -self.smbcheckerr()
        else :
            print 'GPIO Busy'
            return -1

    def smbextrbytes(self, length) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/extwrbytes', 'r')
            s = f.read(int(length)*5+1)
            f.close()
            self.smbreleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def smbextwbytes(self, arg) :
        if self.smbgetlock() :
            f = open('/sys/devices/i2c-0/extwrbytes', 'w')
            f.write(arg)
            f.close()
            self.smbreleaselock()
            return -self.smbcheckerr()
        else :
            print 'GPIO Busy'
            return -1

    def smbparse(self, addr, cmd, rw, data, length, extcmd) :
        self.smbsetaddr(addr)
        if extcmd == None :
            if cmd != None :
                needcmd = 1
                self.smbsetcmd(cmd)
            else :
                needcmd = 0
            if rw == 1 :
                wordCount = data.count(',')+1
                dataList = data.replace(',', ' ')
                self.smbsetnumbytes(str(wordCount))
                if needcmd :
                    return self.smbwritebytes(dataList)
                else :
                    return self.smbsendbytes(dataList)
            else :
                self.smbsetnumbytes(length)
                if needcmd :
                    return self.smbreadbytes(length)
                else :
                    return self.smbrecievebytes(length)
        else :
            self.smbsetcmd(cmd)
            if rw == 1 :
                wordCount = data.count(',')+1
                dataList = data.replace(',', ' ')
                self.smbsetnumbytes(str(wordCount))
                return self.smbextwbytes(dataList)
            else :
                self.smbsetnumbytes(length)
                return self.smbextrbytes(length)
