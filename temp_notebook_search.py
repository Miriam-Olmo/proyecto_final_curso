import json, pathlib
p = pathlib.Path(r"C:\Users\UsuarioM\Documents\proyecto_final_curso\EDA_biblioteca.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
for idx, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") == "code":
        source = "".join(cell.get("source", []))
        if any(s in source for s in ["df =", "pd.merge", "merge(", "df = pd.merge", "df['generos']", "generos"]):
            print(f"CELL {idx}")
            print(source)
            print("=" * 60)
