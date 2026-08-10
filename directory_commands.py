import argparse
import datetime
import os
import sys
import shutil
from pathlib import Path


# ==========================================
# LOGGING HELPER
# ==========================================
def log_action(message: str):
    """
    Logs messages to <Root>/Python_Log/system_log.txt.
    Determines drive root dynamically for cross-platform support.
    """
    try:
        # Determine root drive path ('C:\' on Windows, '/' on POSIX)
        root_dir = Path(Path.cwd().anchor)
        log_dir = root_dir / "Python_Log"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "system_log.txt"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"[Warning] Failed to write to log file: {e}")


# ==========================================
# FOR DELETE OPERATIONS
# ==========================================
def backup_before_delete(target_path: Path):
    """
    Copies a file or folder to <Root>/backups and prefixes it with 'deleted_'.
    """
    root_dir = Path(Path.cwd().anchor)
    backup_dir = root_dir / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_name = f"deleted_{target_path.name}"
    destination = backup_dir / backup_name

    if target_path.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(target_path, destination)
    else:
        shutil.copy2(target_path, destination)

    log_action(f"Backed up '{target_path}' to '{destination}' prior to deletion.")


# ==========================================
# MENU ACTIONS
# ==========================================
def list_directory():
    """Lists files and directories with sizes in the current working directory."""
    current_cwd = Path.cwd()
    print(f"\n--- Directory Listing: {current_cwd} ---")
    try:
        items = list(current_cwd.iterdir())
        if not items:
            print("  (Directory is empty)")
            return

        for item in items:
            item_type = "[DIR] " if item.is_dir() else "[FILE]"
            try:
                size_str = (
                    f"{item.stat().st_size:,} bytes"
                    if item.is_file()
                    else "<DIR>"
                )
            except OSError:
                size_str = "Size Unavailable"

            print(f" {item_type:<6} {item.name:<35} {size_str}")

        log_action(f"Listed directory contents for: {current_cwd}")
    except PermissionError:
        print("Error: Access denied to list this directory.")
    except Exception as e:
        print(f"Error listing directory: {e}")

#==================================
#Changes the Directory
#=============================================
def change_directory():
    """Prompts user and changes current directory."""
    target = input("Enter target directory path: ").strip()
    target_path = Path(target).resolve()

    if ".." in target:
        print("Error: Target path cannot contain '..'")
        return

    if not target_path.exists():
        print("Error: The specified directory does not exist.")
        return
    if not target_path.is_dir():
        print("Error: The path provided is not a directory.")
        return

    try:
        os.chdir(target_path)
        print(f"Directory changed to: {Path.cwd()}")
        log_action(f"Changed directory to: {Path.cwd()}")
    except Exception as e:
        print(f"Error changing directory: {e}")


def copy_item():
    """Prompts and copies a file or directory."""
    src = input("Enter source file or directory path: ").strip()
    src_path = Path(src).resolve()

    if not src_path.exists():
        print("Error: Source path does not exist.")
        return

    dest = input("Enter destination directory path: ").strip()
    dest_dir = Path(dest).resolve()

    if not dest_dir.exists() or not dest_dir.is_dir():
        print(
            "Error: Destination directory does not exist. Operation blocked."
        )
        return

    dest_path = dest_dir / src_path.name

    try:
        if src_path.is_dir():
            if dest_path.exists():
                print(
                    f"Error: Target directory '{dest_path}' already exists."
                )
                return
            shutil.copytree(src_path, dest_path)
            print(f"Successfully copied directory to {dest_path}")
            log_action(f"{src_path.name} was copied to {dest_dir}")
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Successfully copied file to {dest_path}")
            log_action(f"{src_path.name} was copied to {dest_dir}")
    except Exception as e:
        print(f"Error during copy operation: {e}")


def move_item():
    """Prompts and moves a file or directory."""
    src = input("Enter source file or directory path: ").strip()
    src_path = Path(src).resolve()

    if not src_path.exists():
        print("Error: Source path does not exist.")
        return

    dest = input("Enter destination directory path: ").strip()
    dest_dir = Path(dest).resolve()

    if not dest_dir.exists() or not dest_dir.is_dir():
        print(
            "Error: Destination directory does not exist. Operation blocked."
        )
        return

    dest_path = dest_dir / src_path.name

    try:
        shutil.move(str(src_path), str(dest_path))
        print(f"Successfully moved to {dest_path}")
        log_action(f"{src_path.name} was moved to {dest_dir}")
    except Exception as e:
        print(f"Error during move operation: {e}")


def delete_item():
    """Prompts, backs up, and deletes a file or directory."""
    target = input("Enter file or directory path to delete: ").strip()
    target_path = Path(target).resolve()

    if not target_path.exists():
        print("Error: Specified target path does not exist.")
        return

    try:
        # Step 1: Backup and rename
        backup_before_delete(target_path)

        # Step 2: Perform deletion
        if target_path.is_dir():
            shutil.rmtree(target_path)
            print(
                f"Directory '{target_path.name}' deleted (backed up in root 'backups' folder)."
            )
            log_action(f"Directory '{target_path.name}' was deleted.")
        else:
            target_path.unlink()
            print(
                f"File '{target_path.name}' deleted (backed up in root 'backups' folder)."
            )
            log_action(f"File '{target_path.name}' was deleted.")
    except Exception as e:
        print(f"Error during deletion operation: {e}")


# ==========================================
# CLI VALIDATION & ARGPARSE SETUP
# ==========================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Cross-Platform File Manager"
    )

    # Required mode argument (-m) with fixed choices
    parser.add_argument(
        "-m",
        dest="mode",
        required=True,
        choices=["basic", "elevated", "admin"],
        help="Operation mode (required): basic, elevated, or admin",
    )

    # Optional initial directory path argument (-d)
    parser.add_argument(
        "-d",
        dest="directory",
        required=False,
        help="Initial directory path to browse",
    )

    args = parser.parse_args()

    # Validate directory path for '..' folders
    if args.directory:
        if ".." in args.directory:
            print(
                "Error: Provided directory argument path cannot contain '..' relative steps."
            )
            sys.exit(1)

        dir_path = Path(args.directory).resolve()
        if not dir_path.exists() or not dir_path.is_dir():
            print(
                f"Error: Specified startup directory '{args.directory}' does not exist or is not a folder."
            )
            sys.exit(1)

    return args


# ==========================================
# MAIN INTERACTIVE LOOP
# ==========================================
def main():
    args = parse_arguments()
    mode = args.mode.lower()

    # Handle directory startup flag
    if args.directory:
        os.chdir(Path(args.directory).resolve())
        print(f"Set working directory to: {Path.cwd()}")

    log_action(
        f"Session started in '{mode}' mode. Base path: '{Path.cwd()}'"
    )

    while True:
        print("\n" + "=" * 40)
        print(f" FILE MANAGER — [{mode.upper()} MODE]")
        print(f" Current Path: {Path.cwd()}")
        print("=" * 40)
        print("1. List Directory Contents")
        print("2. Change Directory")

        if mode in ["elevated", "admin"]:
            print("3. Copy File or Directory")

        if mode == "admin":
            print("4. Move File or Directory")
            print("5. Delete File or Directory")

        print("Q. Quit Program")
        print("-" * 40)

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            list_directory()
        elif choice == "2":
            change_directory()
        elif choice == "3" and mode in ["elevated", "admin"]:
            copy_item()
        elif choice == "4" and mode == "admin":
            move_item()
        elif choice == "5" and mode == "admin":
            delete_item()
        elif choice == "q":
            print("Exiting File Manager...")
            log_action("Session ended.")
            break
        else:
            #This is for EVERYTHING ELSE
            print("Invalid option or feature restricted in this mode.")


if __name__ == "__main__":
    main()