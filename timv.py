'''
timv script
timv is a Terminal Image Viewer

\033[48;2;r;g;b -> background
\033[38;2;r;g;b -> foreground

Unicode Block Element:
https://www.fileformat.info/info/unicode/block/block_elements/list.htm
'''
from PIL import Image
import os
import sys, getopt

def imgToAnsi(img_file, label=False, percent=100):
    im = Image.open(img_file, mode='r').convert('RGB')

    if percent != 100:
        im = im.resize((int(im.size[0]*(percent/100)), int(im.size[1]*(percent/100))))

    w,h = im.size
    rows,cols = int(h/16), int(w/8)

    for r in range(0, rows):
        for c in range (0, cols):
            box = (c*8, r*16, (c*8)+8, (r*16)+16)
            region = im.crop(box)
            # split in two part the region (top, bottom)
            r_a = region.crop((0,0,8,8))
            r_b = region.crop((0,8,8,16))
            pixels_a, pixels_b = r_a.getcolors(), r_b.getcolors()
            # t -> (count, pixel)
            s_pixels_a = sorted(pixels_a, key=lambda t: t[0], reverse=True)
            s_pixels_b = sorted(pixels_b, key=lambda t: t[0], reverse=True)
            # get the most frequent color
            red_a, green_a, blue_a = s_pixels_a[0][1]
            red_b, green_b, blue_b = s_pixels_b[0][1]
            #print(red, green, blue)
            print('\033[48;2;%i;%i;%i;38;2;%i;%i;%im\u2584\033[0m' % (red_a, green_a, blue_a, red_b, green_b, blue_b), end='')
        print(end='\n')
    #im.show()
    if label:
        base = os.path.basename(img_file)
        print('\033[48;2;0;0;0m%s\033[0m' % base.center(cols))

def printHelp():
    print('timv.py [option] image')
    print('  -l, --label\t Display file name')
    print('  -p, --percent\t Output percentage')
    print('Ex. timv.py -l -p 50 image.jpg')

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hlp:', ['help','label','percent='])
    except getopt.GetoptError:
        printHelp()
        sys.exit()
    
    #img_f = args
    label = False
    percent = 100
    for opt, arg in opts:
        if opt in ('-h', '--help') or len(args) < 1:
            printHelp()
            sys.exit()
        elif opt in ('-l', '--label'):
            label = True
        elif opt in ('-p', '--percent'):
            percent = int(arg)
    
    for f in args:
        imgToAnsi(f, label=label, percent=percent)
