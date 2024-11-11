import signal
from CLI import functions_CLI as f_CLI
from lockf import LockFolder

def handle_exit(signum, frame):
    folder.unlock()
    exit(0)

def main():
    origin = f_CLI.select_origin_folder()
    destination = f_CLI.select_destination_folder()

    global folder
    folder = LockFolder(destination)
    folder.lock()

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    name = f_CLI.select_file_name()
    extension = f_CLI.select_file_extension()

    file_to_move = f_CLI.list_files_to_move(origin, name, extension, starts_with=False, case_sensitive=False)

    for i, (file, move) in enumerate(file_to_move, start=0):
        print(f"{i} - {file} - {move}")

    while True:
        answer = input("Do you want to move this files? (yes/no) ").lower()
        if answer == "yes":
            break
        elif answer == "no":
            return

    f_CLI.move_files_list(origin, destination, file_to_move)

    folder.unlock()

if __name__ == "__main__":
    main()