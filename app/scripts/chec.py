import os
import shutil


def fix_python_filenames_and_clear_cache():
    renamed = []

    # Verifică fișierele .py cu spații
    for filename in os.listdir():
        if filename.endswith(".py") and " " in filename:
            new_name = filename.replace(" ", "_")
            os.rename(filename, new_name)
            renamed.append((filename, new_name))

    # Afișează fișierele redenumite
    if renamed:
        print("🔧 Fișiere redenumite:")
        for old, new in renamed:
            print(f" - {old} → {new}")
    else:
        print("✅ Nu există fișiere .py cu spații în nume.")

    # Șterge __pycache__
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("🧹 Cache-ul '__pycache__' a fost șters.")
    else:
        print("ℹ️ Nu există director '__pycache__'.")


if __name__ == "__main__":
    fix_python_filenames_and_clear_cache()
