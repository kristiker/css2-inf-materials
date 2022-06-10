from pathlib import Path
from os import stat
from zlib import crc32

includeFiles = []
included_but_missing = []
here = Path('.')

def txt_default_normal_flip(fpath: Path):
    crc = 0
    with open(fpath, 'rb', 65536) as ins:
        for _ in range(int((stat(fpath).st_size / 65536)) + 1):
            crc = crc32(ins.read(65536), crc)
    return ('%08X' % (crc & 0xFFFFFFFF)) in ('69D57F2B', '42F60AFF', '005B1D71')

if Path(".gitignore").is_file():
    with open(".gitignore") as fp:
        for line in fp.readlines():
            line = line.strip()
            if not any(line.endswith(ext) for ext in (".vmat", ".txt")) or "*" in line:
                continue
            file = Path(line.strip("!"))
            includeFiles.append(file)
            if not file.exists():
                included_but_missing.append(file)

if Path("custom_resources.txt").is_file():
    with Path("custom_resources.txt").open() as fp:
        for line in fp.readlines():
            line = line.strip()
            custom_resource = Path(line)
            if custom_resource not in includeFiles:
                includeFiles.append(custom_resource)
        
    
for vmat_file in here.glob("**/*.vmat"):
    print("Checking", vmat_file)
    with open(vmat_file, 'r') as fp:
        if fp.readline() != "// THIS FILE IS AUTO-GENERATED\n":
            continue
        if vmat_file not in includeFiles:
            includeFiles.append(vmat_file)

for txt_file in here.glob("**/*.txt"):
    print("Checking", txt_file)
    if txt_default_normal_flip(txt_file):
        continue
    if txt_file not in includeFiles:
        includeFiles.append(txt_file)


with open(".gitignore", "w") as fp:
    fp.writelines(
        ext + "\n" for ext in [
            "*.vmat",
            "*.tga",
            "*.pfm",
            "*.txt",
            "*.json",
            "*.vtex",
            "*.vpost",
            "*.zip",
            "*.7z",
        ]
    )
    fp.writelines(f"!{file.as_posix()}\n" for file in includeFiles)

if included_but_missing:
    print("Files missing from disk but included in git:")
    for file in included_but_missing:
        print(file.as_posix())
