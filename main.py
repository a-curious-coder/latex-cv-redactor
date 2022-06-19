""" Document redactor """
import sys
import zipfile
import os
import threading


def unzip_latex_project(zip_file):
    """ Unzip the latex project

    Args:
        zip_file (str): The path to the zip file
    """
    # If file isn't a zip file
    if not zip_file.endswith(".zip"):
        print("[INFO]\tFile is not a zip file")
        print("[INFO]\tAssuming it's a folder with LaTeX files")
        input()
        return
    # Unzip zip_file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(zip_file.replace('.zip', ''))


def redact_document(work_folder, redact):
    """ Redact the document

    Args:
        work_folder (str): The path to the work folder
    """
    # Declare blank dictionary
    keywords = {}
    # Read keywords
    with open("keywords.txt", "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(":")
                # Remove spaces from key and value
                key = key.replace(" ", "")
                value = value.replace(" ", "")
                # Replace all instances of key with value
                keywords[key] = value
                # Create all case version of keys and value
                keywords[key.upper()] = value.upper()
                keywords[key.lower()] = value.lower()
                keywords[key.capitalize()] = value.capitalize()
                # Count number of chars in key
    # Signals when document actually begins
    document_begun = False
    # Replace all the keywords in all .tex files in the work_folder
    if os.name == "nt":
        for path, _, files in os.walk(work_folder):
            for file in files:
                # If file is main.tex
                if file == "main.tex":
                    # Write "hello" at top of file
                    with open(path + "\\" + file, "r", encoding="utf-8") as f:
                        contents = f.read()
                        # For each line in contents
                        for line in contents.split("\n"):
                            if document_begun:
                                replacement = "\\usepackage{censor}" + \
                                    "\n" + line
                                # Add censor library after the document begins
                                contents = contents.replace(
                                    line, replacement)
                                # write contents to file
                                with open(path + "\\" + file, "w", encoding='utf-8') as f:
                                    f.write(contents)
                                break
                            # if line contains \documentclass
                            if "\\documentclass" in line:
                                document_begun = True

                    with open(path + "\\" + file, "w", encoding='utf-8') as f:
                        f.write(contents)

                if file.endswith(".tex"):
                    with open(os.path.join(path, file), "r", encoding='utf-8') as f:
                        contents = f.read()

                    for keyword in keywords.keys():
                        if file == "main.tex":
                            contents = contents.replace(
                                keyword, keywords[keyword])
                        else:
                            if redact:
                                # If there's a link in the document
                                if "\\href" in contents:
                                    # Find which line contains the link
                                    for line in contents.split("\n"):
                                        if "\\href" in line:
                                            # Redact the link
                                            redacted_link = redact_link(line)
                                            # Replace the link with the redacted link
                                            contents = contents.replace(
                                                line, redacted_link)
                                else:
                                    contents = contents.replace(
                                        keyword, f"\\censor{{{keyword}}}")
                            else:
                                contents = contents.replace(
                                    keyword, keywords[keyword])

                    with open(os.path.join(path, file), "w", encoding="utf-8") as f:
                        f.write(contents)


def redact_link(line):
    """ Redacts link lines in LaTeX file

    Args:
        line (str): The line to redact

    Returns:
        str: The redacted line
    """
    # If line already has \censor
    if "\\censor" in line:
        return line
    # Store everything before \\href
    before_href = line.split("\\href")[0]
    # Remove before_href from line
    line = line.replace(before_href, "")
    # If line contains \href
    if "\\href" in line:
        # Split line into parts
        parts = line.split("{")
        # Get the link
        link = parts[2].split("}")[0]
        # replace { with ""
        link = link.replace("{", "")
        # Replace link with censor
        line = parts[2].replace(link, "{\\censor{" + link + "}")
    # input(line)
    return before_href + line


def compile_redacted_project(work_folder):
    """ Compile LaTeX project

    Args:
        work_folder (str): The path to the work folder
    """
    print(f"[INFO]\tCompiling project in {work_folder}")
    # Compile the project
    os.system("cd " + work_folder +
              " && pdflatex -interaction=nonstopmode main.tex")

    if os.name == "nt":
        # Move pdf file from work_folder to current directory
        os.system("move " + work_folder + r"\main.pdf " +
                  os.path.dirname(os.path.abspath(__file__)))
    if os.name == "posix":
        # Move the pdf file from work_folder to the parent folder
        os.system("mv " + work_folder + "/main.pdf " +
                  os.path.dirname(work_folder))


def cleanup(work_folder):
    """ Cleanup the work folder """
    # If operating system is windows
    if os.name == 'nt':
        # Remove the unziped folder
        os.system("rmdir /s /q " + work_folder)
    # If operating system is linux or mac
    if os.name == 'posix':
        # Remove the unziped folder
        os.system("rm -rf " + work_folder)


def menu(args=None):
    """ Menu for redactor

    Args:
        args (list): The arguments passed to the program
    """
    if args is None:
        args = []
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Read title.txt
    with open("title.txt", "r", encoding='utf-8') as file:
        title = file.read()
    print(title)
    if len(args) > 0:
        # Menu
        print("\n\n")
        print("[1]\tRedact keywords in document")
        print("[2]\tReplace keywords in document")
        print("[3]\tExit")
        print("\n\n")
        choice = input("Enter your choice > ")
    else:
        print("\n\n[INFO]\tUsage is: python main.py <name of zip file>\n\n")
        return

    if choice == "1":
        print("\n\n[INFO]\tRedacting keywords...")
        redact = True
    elif choice == "2":
        print("\n\n[INFO]\tReplacing keywords...")
        redact = False
    elif choice == "3" or "exit":
        print("\n\n[INFO]\tExiting...\n\n")
        sys.exit(0)
    else:
        print("Invalid choice")
        menu(args)

    if len(args) > 0:
        # check if arg ends with .zip
        try:
            unzip_latex_project(sys.argv[1])
            unzip_folder = sys.argv[1].replace('.zip', '')
            # Execute redactor on separate thread
            thread = threading.Thread(
                target=redact_document, args=(unzip_folder, redact, ))
            thread.start()
            # Wait for thread to finish
            thread.join()
            # redact_document(unzip_folder)
            compile_redacted_project(unzip_folder)
            # cleanup(unzip_folder)
        except Exception as e:
            print(f"[ERR]\t{e}")
            sys.exit(1)
        print(
            "[INFO]\tDocument redacted and compiled successfully. Press enter to exit...")
        sys.exit(1)
    else:
        print("Usage: python main.py <latex project directory>")
        sys.exit(1)
    menu(args)


def main():
    """ Main function """
    # If keywords.txt doesn't exist
    if not os.path.isfile("keywords.txt"):
        print("keywords.txt not found")
        sys.exit(1)
    args = sys.argv
    if len(args) > 1:
        menu(args)
    else:
        menu()


if __name__ == "__main__":
    main()
