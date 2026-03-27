import time

def retry(func,attempts=3):

    for i in range(attempts):

        try:

            return func()

        except:

            time.sleep(3*(i+1))

    raise Exception("All retries failed")