from pathlib import Path

top = "\n".join([
        "/*",
        "!.gitignore",
        "!gitinclude-modified-vmats-only.py",
    ])
top += "\n"

includefiles = []
here = Path('.')

with open(".gitignore") as fr:
    for line in fr.readlines():
        if line not in top.splitlines(True):
            line = line.strip()
            if not line.endswith(".vmat"):
                continue
            includefiles.append(Path(line))
    
for vmat_file in here.glob("**/*.vmat"):
    print("Checking", vmat_file)
    with open(vmat_file, 'r') as fp:
        if fp.readline() == "// THIS FILE IS AUTO-GENERATED\n":
            includefiles.append(vmat_file)
        elif vmat_file in includefiles:
            includefiles.remove(vmat_file)

alreadyin_folders = []
with open(".gitignore", "w") as fw:
    fw.write(top)
    for file in includefiles:
        if file == here:
            continue
        for shit in reversed(file.parents):
            if shit in alreadyin_folders:
                continue
            if shit == here:
                continue
            alreadyin_folders.append(shit)
            fw.write(f"!/{Path(shit).as_posix()}\n")
            fw.write(f"/{Path(shit).as_posix()}/*\n")
        fw.write(f"!/{file.as_posix()}\n")
    fw.write("\n")
