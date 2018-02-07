import subprocess
from datetime import datetime
from threading import Thread, Lock
import logging

logging.basicConfig(filename='alerts.log',level=logging.INFO)
PAGES = 3621
THREADS= 100

def OCR(page):
    for i in range(page, PAGES, PAGES/100):
        page_number = page + i
        info('starting thread {}!'.format(page_number))
        print 'staring thread {}'.format(page_number)
        pdf_name = 'wong/wong-page{}.pdf'.format(page_number)
        tiff_name = 'tiff/img-page{}.tiff'.format(page_number)
        save_name = 'output/wong{}.txt'.format(page_number)

        convert_to_tiff_command = "convert -density 300 {} -depth 8 {}".format(pdf_name, tiff_name)
        ocr_command = "tesseract {} {}".format(tiff_name, save_name)

        try:
            info('TO TIFF: Thread {} starting...'.format(page_number))
            process = subprocess.Popen(convert_to_tiff_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            info('output, error {} {}'.format(output, error))
            info('TO SAVE FILE: Thread {} starting...'.format(page_number))
            process = subprocess.Popen(ocr_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            info('output, error {} {}'.format(output, error))
        except Exception as e:
            exc(e)
            print 'hit exception'

def info(msg):
    with Lock():
        date = datetime.now()
        logging.info("[{}]: {}".format(date, msg))

def exc(msg):
    with Lock():
        date = datetime.now()
        logging.exception("[{}]: {}".format(date, msg))

def main():
    print 'hi'
    for i in range(THREADS):
        Thread(target=OCR, args=(i,)).start()


if __name__ == "__main__":
    main()
