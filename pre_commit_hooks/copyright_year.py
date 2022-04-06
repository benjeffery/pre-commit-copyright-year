import sys
import subprocess
import datetime
from itertools import islice

def main():
    for filename in sys.argv[1:]:
        result = subprocess.run(["git","status",filename], capture_output=True, text=True)
        try:
            if "Changes to be committed" in result.stdout:
                year = datetime.datetime.now().year
            elif "nothing to commit" in result.stdout:
                year = subprocess.run(['git', 'log', '-1', '--format="%as"', '--', filename], capture_output=True, text=True).stdout[1:5]
            else:
                continue
            with open(filename, "r") as f:
                for line in islice(f.readlines(),4):
                    if "Copyright" in line:
                        if str(year) in line:
                            break
                        else:
                            print(filename, 'has incorrect copyright year of "' , line.strip(), '" it should contain', year)
                            return 1

        except:
            print("Error in year checking - skipping")
            pass
    return 0
