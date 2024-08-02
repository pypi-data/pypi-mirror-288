import datetime
import filecmp
import pathlib
import signal
import tempfile
import urllib.parse

import requests


class OIGrader:
    TIME_TO_LIVE = 4

    def handler(self, sig, frame):
        raise TimeoutError()

    def solve(self, instream, outstream):
        raise NotImplementedError("Please implement code logic")

    def measure(self, bucket: str, uuid: str, item: str):
        correct, elapsed = None, None

        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)

            base = bucket + "/" + uuid + "/"

            # download in file
            with (folder / (item + ".in")).open("wb") as stream:
                url = urllib.parse.urljoin(base, item + ".in")
                res = requests.get(url)
                stream.write(res.content)

            # download out file
            with (folder / (item + ".out")).open("wb") as stream:
                url = urllib.parse.urljoin(base, item + ".out")
                res = requests.get(url)
                stream.write(res.content)

            # execute user code with time bound
            start = datetime.datetime.now()
            try:
                signal.signal(signal.SIGALRM, self.handler)
                signal.alarm(self.TIME_TO_LIVE)

                with (folder / (item + ".in")).open("r") as instream, (
                    folder / (item + ".act")
                ).open("w") as outstream:
                    self.solve(instream, outstream)
            except TimeoutError as e:
                correct = "TLE"
            except:
                correct = "RE"
            finally:
                signal.alarm(0)
            end = datetime.datetime.now()
            elapsed = int((end - start).total_seconds() * 1000)  # milliseconds

            # compare user output with the baseline
            if correct is None:
                if filecmp.cmp(
                    folder / (item + ".act"), folder / (item + ".out"), shallow=False
                ):
                    correct = "AC"
                else:
                    correct = "WA"

        return {"state": correct, "execute_time": elapsed}

    def grade(self, bucket: str, uuid: str, items: list):
        """
        `url` is the path of test data while items are the file names (without .in or .out)
        """
        result = []
        for item in items:
            metric = self.measure(bucket, uuid, item)
            result.append(metric)

        return result
