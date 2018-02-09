import subprocess
from datetime import datetime
from threading import Thread, Lock
import logging

logging.basicConfig(filename='alerts.log',level=logging.INFO)
PAGES = 3679
PAGES = 20
THREADS = 10
PAGE_PER_THREAD = PAGES / THREADS

def OCR_on_pages(pages):
    for i in pages:
        OCR_one_page(i)

def OCR(thread_number):
    for i in range(PAGE_PER_THREAD*thread_number, PAGE_PER_THREAD*thread_number+PAGE_PER_THREAD):
        print 'about to OCR page {}'.format(i)
        page_number = i
        OCR_one_page(page_number)

def OCR_one_page(page_number):
    pdf_name = 'wong/wong-page{}.pdf'.format(page_number)
    jpg_name = 'jpg/img-page{}.jpg'.format(page_number)
    save_name = 'jpg_output/wong{}.txt'.format(page_number)

    convert_to_jpg_command = "convert -density 300 {} -depth 8 {}".format(pdf_name, jpg_name)
    ocr_command = "tesseract {} {}".format(jpg_name, save_name)
    remove_jpg = "rm {}".format(jpg_name)

    try:
        info('TO jpg: Thread {} starting...'.format(page_number))
        process = subprocess.Popen(convert_to_jpg_command.split())
        output, error = process.communicate()
        info('output, error {} {}'.format(output, error))
        info('TO SAVE FILE: Thread {} starting...'.format(page_number))
        process = subprocess.Popen(ocr_command.split())
        output, error = process.communicate()
        info('output, error {} {}'.format(output, error))
        process = subprocess.Popen(remove_jpg.split())
        output, error = process.communicate()
        info('output, error {} {}'.format(output, error))
        info('REMOVING JPG: {}...'.format(jpg_name))
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
        Thread(target=OCR, args=(i+1,)).start()


if __name__ == "__main__":
    main()
