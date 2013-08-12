class mdio_lib :

    def mdiosetphy(self, phy) :
        f = open('/sys/devices/platform/MDIO.0/PHY', 'w')
        f.write(phy)
        f.close()
        return 0

    def mdiosetreg(self, reg) :
        f = open('/sys/devices/platform/MDIO.0/reg', 'w')
        f.write(reg)
        f.close()
        return 0

    def mdiosetc45(self, c45) :
        f = open('/sys/devices/platform/MDIO.0/c45', 'w')
        f.write(c45)
        f.close()
        return 0

    def mdiogetlock(self) :
        f = open('/sys/devices/platform/MDIO.0/lock', 'r')
        s = f.read(1)
        f.close()
        if int(s) == 1 :
            return 1
        return 0

    def mdioreleaselock(self) :
        f = open('/sys/devices/platform/MDIO.0/lock', 'w')
        f.write('0')
        f.close()
        return 0

    def mdioread(self) :
        if self.mdiogetlock() :
            f = open('/sys/devices/platform/MDIO.0/data', 'r')
            s = f.read(8)
            f.close()
            self.mdioreleaselock()
            return s.rstrip()
        else :
            print 'GPIO Busy'
            return -1

    def mdiowrite(self, arg) :
        if self.mdiogetlock() :
            f = open('/sys/devices/platform/MDIO.0/data', 'w')
            f.write(arg)
            f.close()
            self.mdioreleaselock()
            return 0
        else :
            print 'GPIO Busy'
            return -1

    def mdioparse(self, phy, addr, reg, rw, data) :
        self.mdiosetphy(phy)
        if addr == None :
            c45 = 0
        else :
            c45 = 1
        self.mdiosetc45(str(c45))
        conv = 0
        if c45 == 1 :
            conv = int(addr) << 16
        conv += int(reg)
        self.mdiosetreg(str(conv))
        if rw == 1 :
            self.mdiowrite(data)
        else :
            return self.mdioread()
        return 0
