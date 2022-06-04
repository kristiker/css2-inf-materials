from pathlib import Path

ignoreMaterials = []
here = Path('.')

with open(".gitignore") as fr:
    for line in fr.readlines():
        line = line.strip()
        if not line.endswith(".vmat"):
            continue
        ignoreMaterials.append(Path(line))
    
for vmat_file in here.glob("**/*.vmat"):
    print("Checking", vmat_file)
    with open(vmat_file, 'r') as fp:
        if fp.readline() == "// THIS FILE IS AUTO-GENERATED\n":
            continue
        if vmat_file not in ignoreMaterials:
            ignoreMaterials.append(vmat_file)

with open(".gitignore", "w") as fw:
    fw.writelines(
        ext + "\n" for ext in [
            "*.tga",
            "*.pfm",
            "*.txt",
            "*.json",
            "*.vtex",
            "*.vpost",
        ]
    )
    fw.writelines(file.as_posix()+'\n' for file in ignoreMaterials)
