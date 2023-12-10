from PIL import ImageGrab
from os import environ
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, Process
from dotenv import load_dotenv
from time import sleep
from airtable import AirtableInterface
# import json

load_dotenv()


def now():
    return datetime.now().isoformat()


def process_frame(img_buffer, lock, screenshot_folder):
    try:
        screenshot_dt = now()

        print(f"[{now()}] Grabbing Screenshot")
        img = ImageGrab.grab(all_screens=True)

        print(f"[{now()}] Saving Image")
        filename = f"{screenshot_folder}/screenshot_{screenshot_dt}.jpg"
        img.convert("RGB").save(filename, dpi=(100, 100), optimize=True)

        if environ["IN_PROCESS_GPT"]:
            lock.acquire()
            try:
                img_buffer.append(filename)
            finally:
                lock.release()

    except Exception as e:
        print(f"[{now()}] Exception: {str(e)}")


def submit_gpt4_vision_request(img_buffer):
    print("BATCH PROCESSING IMAGES : %s" % img_buffer)
    # TODO - call understanding.py
    
    # TODO - save GPT4 vision output in Airtable
    pass


def run_gpt_ps(img_buffer, tmp_buffer, lock):
    ocr_interval = int(environ["OCR_INTERVAL"])
    while True:
        sleep(ocr_interval)
        lock.acquire()
        try:
            if img_buffer:
                while img_buffer:
                    tmp_buffer.append(img_buffer.pop(0))

                # print("Cleared img_buffer : length from %s --> to %s" % (len(tmp_buffer), len(img_buffer)))
        finally:
            lock.release()
            submit_gpt4_vision_request(tmp_buffer)

            while len(tmp_buffer) > 0:
                tmp_buffer.pop()


def main():
    max_workers = int(environ["MAX_WORKERS"])
    worker_sleep_duration = int(environ["SLEEP_DURATION"])
    screenshot_folder = environ["SCREENSHOTS_FOLDER"]

    with Manager() as manager:
        lock = manager.Lock()
        img_buffer, tmp_buffer = manager.list(), manager.list()

        if environ["IN_PROCESS_GPT"]:
            gpt4_ps = Process(target=run_gpt_ps, args=(img_buffer, tmp_buffer, lock))
            gpt4_ps.start()

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            while True:
                print(f"[{now()}] Starting thread")
                executor.submit(process_frame, img_buffer, lock, screenshot_folder)
                print(f"[{now()}] Sleeping {worker_sleep_duration}s")
                sleep(worker_sleep_duration)


if __name__ == "__main__":
    main()
