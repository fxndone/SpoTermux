try:
    import requests
except ImportError:
    raise Exception("\"requests\" module needed, please install it !")
import zipfile
import shutil
import io
import os

RAW_GITHUB_URL = "https://raw.githubusercontent.com/fxndone/SpoTermux/"
GITHUB_URL     = "https://github.com/fxndone/SpoTermux/"

def check_for_updates():
    print("[+] Checking for version, please wait...")
    if os.path.isfile(".files/.version"):
        with open(".files/.version", "r") as f:
            my_v = f.read().replace("\n", "").replace("\t", "").replace("\r", "")
    else:
        my_v = "0.0"
    try:
        requests.get("https://google.com")
    except requests.exceptions.ConnectionError:
        print("[!] Bad internet connection detected !")
        print("[!] Update failed, please retry later")

        return
    current_v = requests.get(RAW_GITHUB_URL+"master/.files/.version").text.strip()


    print()
    print("[+] Current version      : ", end='')
    print(my_v)
    print("[+] Last aviable version : ", end='')
    print(current_v)
    print()

    if my_v != current_v:
        chx = input("[?] Do you want to update SpoTermux ? (Y/N) : ")
        while not chx.upper() in ("Y", "N"):
            chx = input(">> ")
        if chx.upper() == "N":
            return
        else:
            response = requests.get(GITHUB_URL+"archive/master.zip")
            if response.status_code == 200:
                zip_content = response.content
                try:
                    with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
                        for member in zip_file.namelist():
                            filename = os.path.split(member)
                            if not filename[1]:
                                continue
                            new_filename = os.path.join(
                                filename[0].replace("SpoTermux-main", "."),
                                filename[1])
                            new_dir = os.path.dirname(new_filename)
                            if not os.path.isdir(new_dir):
                                os.mkdir(new_dir)
                            source = zip_file.open(member)
                            target = open(new_filename, "wb")
                            with source, target:
                                shutil.copyfileobj(source, target)
                    input("[+] Update complete, please press enter...")
                    print("[+] Please restart SpoTermux")
                    return 1
                except:
                    return
            else:
                print("[!] Bad response from github, please retry later")
                return
    else:
        print("[+] You're up to date !")