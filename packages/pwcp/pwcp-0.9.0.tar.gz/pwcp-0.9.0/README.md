# pwcp
Python with C preprocessor

## Installation
`pip install git+https://github.com/solaluset/pwcp`

## Running
`pwcp <file>`

`pwcp -m <module>`

Or run built-in `code` module to start interactive console:

`pwcp -m code`

## Why?
For fun!

## How to use it?
The extension for files that need to be preprocessed is `.ppy` (pre-python).
You can start by creating `hello.ppy` and putting there something like

    #define hello "Hello "
    #define world "world!"
    print(hello world)

Then run it

    ~ $ pwcp hello.ppy
    Hello world!

Congratulations! You've run your first program with PWCP.

### Extension for header files?
Suggested extension is `.pyh` (python header), but technically you can use whatever you like.

### What about comments?
The suggested way to write comments in `.ppy` (and `.pyh`) files is `/* comment */`

`//` is not a comment as it's floor division in Python and `#` indicates preprocessor directives.

### Does it work with pure Python?
Of course. It works like an extension allowing you to run and import `.ppy` files. You can import `.ppy` file in `.py` file and vice versa.

Feel free to submit an issue if something doesn't work.
