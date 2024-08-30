from dotenv import load_dotenv
import os
import subprocess
from mcrcon import MCRcon as r
from mcstatus import JavaServer


def sort_md(file: str):
    file_path = "./messages/" + file + ".md"
    new_file_path = "./messages/" + file + "_sorted.md"
    md_file = open(file_path, "r")
    md_text = md_file.readlines()
    md_text.sort()
    md_file.close()
    sorted_md_file = open(new_file_path, "w")
    sorted_md_file.writelines(md_text)


def read_md(file: str) -> str:
    file = "./messages/" + file + ".md"
    md_file = open(file, "r")
    md_text = md_file.readlines()
    md_file.close()
    parsed_text = ""
    for text in md_text:
        parsed_text += text
    return parsed_text


def check_status() -> bool:
    """Checks status of server.

    Returns:
        Server status
    """
    try:
        IP = os.getenv("IP")
        server = JavaServer.lookup("localhost")
        status = server.status()
        return True
    except:
        return False


def start_server() -> str:
    """Starts server in a new terminal.

    Returns:
        Status of server is turning on or not.
    """
    return_str = ""
    if check_status():
        return_str = "Server Already Running!"
    else:
        load_dotenv()
        DIR_PATH = os.getenv(r'DIR_PATH')
        FILE_PATH = os.getenv('FILE_PATH')

        print("Starting Server...")
        os.chdir(DIR_PATH)
        subprocess.Popen(["start", "cmd", "/k", FILE_PATH], shell=True)
        return_str = "Server Started! Wait a ~30 seconds for the server to fully boot up."
    return return_str


def send_cmd(cmd: str, arg: str = None):
    # TODO: Investigate reducing complexity of function by breaking it up.
    """Runs incoming command through mcr.

    Args:
        cmd: different command phrases to start different process

    Returns:
        Status of commands run.
    """
    return_str = ""
    if check_status() == False:
        return_str = "Server Offline"
        return return_str
    else:
        IP = os.getenv("IP")
        server = JavaServer.lookup("localhost")
        status = server.status()
        with r('localhost', 'pass', 25575) as mcr:
            if cmd == "status":
                if check_status == False:
                    return_str = "Server Offline"
                else:
                    return_str = f"Server is Up and Running with a ping of {status.latency} ms!"
                    return_str += f"\nPlayers Currently Online [{status.players.online}]: "
                    query = server.query()
                    return_str += f"\nThe server has the following players online: {', '.join(query.players.names)}"
                    print(return_str)
                return return_str

            if cmd == "save":
                print("Saving World ...")
                resp = mcr.command('/save-all')
                return_str = "World Saved!"
                return return_str

            if cmd == "quit":
                print("Shuting Down Server ...")
                print("Saving World ...")
                resp = mcr.command('/save-all')
                print("World Saved!")
                resp = mcr.command('/stop')
                return_str = "Server Stopped"
                return return_str

            if cmd == "kick":
                print(f"Kicking {arg}")
                resp = mcr.command(f'/kick {arg}')
                return_str = f"{arg} kicked!"
                return return_str


if __name__ == "__main__":
    sort_md("modlist_1_2")
    # start_server()
    # send_cmd("status")
