class gpio_lib :

    def gpiosetpath(self, gpio, devatt) :
        s = '/sys/class/gpio/gpio'
        s += gpio + devatt
        return s

    def gpioexport(self, gpio) :
        f = open('/sys/class/gpio/export', 'w')
        f.write(gpio)
        f.close()
        return 0

    def gpiounexport(self, gpio) :
        f = open('/sys/class/gpio/unexport', 'w')
        f.write(gpio)
        f.close()
        return 0

    def gpiosetdir(self, gpio, iodir) :
        f = open(self.gpiosetpath(gpio, '/direction'), 'w')
        f.write(iodir)
        f.close()
        return 0

    def gpiogetdir(self, gpio) :
        f = open(self.gpiosetpath(gpio, '/direction'), 'r')
        ret = f.read(3)
        f.close()
        return ret

    def gpiosetval(self, gpio, val) :
        self.gpioexport(gpio)
        self.gpiosetdir(gpio, 'out')
        f = open(self.gpiosetpath(gpio, '/value'), 'w')
        f.write(val)
        f.close()
        self.gpiounexport(gpio)
        return 0

    def gpiogetval(self, gpio) :
        self.gpioexport(gpio)
        self.gpiosetdir(gpio, 'in')
        f = open(self.gpiosetpath(gpio, '/value'), 'r')
        ret = f.read(1)
        f.close()
        self.gpiounexport(gpio)
        return ret

    def gpiodirin(self, gpio) :
        self.gpioexport(gpio)
        f = open(self.gpiosetpath(gpio, '/direction'), 'w')
        f.write('in')
        f.close()
        self.gpiounexport(gpio)
        return 0
