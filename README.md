# LaTeX CV Redactor
Made this because I was fedup of manually changing my personal info for generic stuff every time I wanted a CV review from the nefarious strangers I talk to online ;)

NOTE: Limited testing on MACOS and Linux... Let me know if anything's not working. Cheers

![Redacted CV Example](images/cv_example.png)
## Prerequisites
---
You will need pdflatex installed on your machine
* [PdfLaTeX](https://www.latex-project.org/downloads/)


## Setup
---
Setup  and initialise virtual environment
```
# Setup virtual environment
virtualenv .venv

# Activate virtual environment OSX/Linux
source .venv/bin/activate

# Activate virtual environment Windows
.venv\Scripts\activate
```

Download/install requirements.txt
```
pip install -r requirements.txt
```

Go to your LaTeX project and download the .zip source file
![Download](images/download.png)
Save the .zip file to this project's working directory

Before running the script, you need to create a file called "keywords.txt" in the same directory as the .zip file. This file should contain a list of keywords that you want the script to search for and replace in your CV. Write the keywords and replacement words in the following format:

```
keyword1 : replacement1
keyword2 : replacement2
keyword3 : replacement3
# NOTE: spaces between the colon and the replacement word aren't necessary
```
NOTE: I still need to adapt the program to recognise a list of keywords rather than key/value pairs

Run main.py and provide the zip file name as the argument
```
python main.py <zip file name>
python main.py <folder name>
```

Any issues, feel free to contact me on [Twitter](https://twitter.com/CuriousCoder4)
