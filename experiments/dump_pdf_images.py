from os.path import join, dirname, abspath
from os import listdir

''' 
Stole this from Ned Batchelder: 
http://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html

It seems to work for most of the PDFs that we were given by Jacob Fenton
'''

pdf_dir = join(abspath(dirname(__file__)), 'raleigh_1314/raleigh_pdfs')


def grok_pdf(name):
    pdf = file(join(pdf_dir, name), 'rb').read()
    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")
        
        istart += startfix
        iend += endfix
        print "JPG %d from %d to %d" % (njpg, istart, iend)
        jpg = pdf[istart:iend]
        jpgfile = file("dumped_images/%s_jpg%d.jpg" % (name.rsplit('.', 1)[0], njpg), "wb")
        jpgfile.write(jpg)
        jpgfile.close()
        
        njpg += 1
        i = iend

if __name__ == "__main__":
    for name in listdir(pdf_dir):
        grok_pdf(name)
