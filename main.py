import subprocess

if __name__ == "__main__":
    subprocess.Popen(
        ["start", "cmd", "/k", "python ./taus_bot.py"], shell=True)
