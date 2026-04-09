import subprocess
import sys

def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    action = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()

    if action in ("extract", "all"):
        run(["pybabel", "extract", "-F", "babel.cfg", "-o", "messages.pot", "."])

    if action in ("init",):
        # Solo para primera vez, si no existen catálogos
        run(["pybabel", "init", "-i", "messages.pot", "-d", "app/translations", "-l", "es"])
        run(["pybabel", "init", "-i", "messages.pot", "-d", "app/translations", "-l", "en"])
        run(["pybabel", "init", "-i", "messages.pot", "-d", "app/translations", "-l", "fr"])

    if action in ("update", "all"):
        run(["pybabel", "update", "-i", "messages.pot", "-d", "app/translations"])

    if action in ("compile", "all"):
        run(["pybabel", "compile", "-d", "app/translations"])

if __name__ == "__main__":
    main()
