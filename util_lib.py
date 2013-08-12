class util_lib :
    def printhexgrid(self, offset, datastr) :
        datalist = datastr.rstrip().split(' ')
        print '        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f'
        i = offset>>4<<4
        j = offset%16
        print '{:05x}'.format(int(i)), ':',
        for x in range(0, j):
            print '  ',
        for num in datalist :
            if j > 15 :
                i += 16
                print ''
                print '{:05x}'.format(i), ':',
                j = 0
            print '{:02x}'.format(int(num, 16)),
            j += 1
