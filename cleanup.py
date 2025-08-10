import os
import re

# === CONFIG ===
folder_path = os.getcwd()  #os.path.expanduser("~/Downloads")  # change as needed
DRY_RUN = True  # set to False to actually perform deletions/renames
# ==============

pattern = re.compile(r"^(?P<base>.+?)(?: \((?P<num>\d+)\))?(?P<ext>\.[^.]+)$")

# group files by (base_lower, ext_lower) to be case-insensitive
groups = {}

for fname in os.listdir(folder_path):
    fpath = os.path.join(folder_path, fname)
    if not os.path.isfile(fpath):
        continue
    m = pattern.match(fname)
    if not m:
        continue
    base = m.group("base")
    num = int(m.group("num") or 0)
    ext = m.group("ext")
    key = (base.lower(), ext.lower())
    groups.setdefault(key, []).append((num, fname))

if not groups:
    print("No matching files found.")
else:
    for key, versions in groups.items():
        # sort by number (0 = no suffix)
        versions.sort(key=lambda x: x[0])
        highest_num, highest_file = versions[-1]

        # files to delete: everything except the highest_file
        files_to_delete = [fname for (_, fname) in versions if fname != highest_file]

        # 1) delete older versions first
        for fname in files_to_delete:
            path = os.path.join(folder_path, fname)
            if DRY_RUN:
                print(f"[DRY RUN] Would delete: {fname}")
            else:
                try:
                    os.remove(path)
                    print(f"Deleted: {fname}")
                except FileNotFoundError:
                    print(f"Not found (skipped): {fname}")
                except Exception as e:
                    print(f"Error deleting {fname}: {e}")

        # 2) rename the highest-numbered file to the base name (if needed)
        m_high = pattern.match(highest_file)  # should match
        base_orig = m_high.group("base")
        ext_orig = m_high.group("ext")
        final_name = base_orig + ext_orig
        src = os.path.join(folder_path, highest_file)
        dst = os.path.join(folder_path, final_name)

        if highest_file == final_name:
            print(f"Kept (already original): {final_name}")
        else:
            if DRY_RUN:
                print(f"[DRY RUN] Would rename: {highest_file} -> {final_name}")
            else:
                # If dst somehow exists (unlikely because we deleted other versions),
                # remove it before renaming to avoid errors.
                if os.path.exists(dst):
                    try:
                        os.remove(dst)
                    except Exception as e:
                        print(f"Could not remove existing {final_name}: {e}")
                        continue
                try:
                    os.rename(src, dst)
                    print(f"Renamed: {highest_file} -> {final_name}")
                except Exception as e:
                    print(f"Error renaming {highest_file}: {e}")

    print("Done.")
