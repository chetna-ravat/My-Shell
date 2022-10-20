import os
from signal import SIGKILL

DEBUG = False

def shell_icon(start=False):
    if start:
        print('''Provide program name and args to run like you would in a shell.\nExamples:\n\nls\nls -al\ncat file1\npwd\n\nShell Started''')
    print("$ ", end="")

def read_command(cmd):
    try:
        cmd[0] = input()
        return True
    except EOFError:
        print()
        return False

def main():
    cmd = [""]
    shell_icon(True)
    while read_command(cmd):

        # It doesn't make sense to go through the whole process if cmd is empty
        if len(cmd[0]) > 0:
            
            try:
                # create new process
                pid = os.fork()
            except OSError:
                raise("OS error while creating child process")
            
            if pid == 0: # Child process
                command = cmd[0].split()
                program = command[0]
                arguments = command[1:]

                if DEBUG: print(f"LOG: Executing '{program} {''.join(arguments)}' in child process")

                try:
                    # Execute command in shell
                    os.execlp(program, program, *arguments)
                except OSError:
                    child_pid = os.getpid()
                    print(f"We may not support '{cmd[0]}' or you have used command incorrectly.")
                    if DEBUG: print(f"Killing pid {child_pid}")
                    os.kill(child_pid, SIGKILL)
                    
            else: # parent process
                # Wait for command execution to be completed
                if DEBUG: print(f"LOG: Wating for child with pid {pid} to be completed")

                (wait_pid, wait_status) = os.waitpid(pid, 0)
                if wait_pid != pid:
                    raise(f"wait error for {pid}: {wait_status}")
        shell_icon()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Let collect shell and run after them')
    parser.add_argument('-v', action='store_true', help='verbose mode')

    args = parser.parse_args()
    if args.v:
        DEBUG=True
    main()