from pathlib import Path
from os import stat
from zlib import crc32

includeFiles = []
here = Path('.')

def txt_default_normal_flip(fpath: Path):
    crc = 0
    with open(fpath, 'rb', 65536) as ins:
        for _ in range(int((stat(fpath).st_size / 65536)) + 1):
            crc = crc32(ins.read(65536), crc)
    return ('%08X' % (crc & 0xFFFFFFFF)) in ('69D57F2B', '42F60AFF', '005B1D71')

if Path(".gitignore").is_file():
    with open(".gitignore") as fr:
        for line in fr.readlines():
            line = line.strip()
            if not any(line.endswith(ext) for ext in (".vmat", ".txt")) or "*" in line:
                continue
            includeFiles.append(Path(line.strip("!")))
    
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

with open(".gitignore", "w") as fw:
    fw.writelines(
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
    fw.writelines(f"!{file.as_posix()}\n" for file in includeFiles)
