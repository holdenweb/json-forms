# json-forms: collect JSON data in a user-friendly way

The main current purpose of this document is to explain how
to get your computer to run this software. Follow these steps.

1.  Clone this repository into a directory of your choice (in this
    example, `json-forms`:

        git close https://github.com/holdenweb/json-forms.git json-forms

2.  Switch to the directory you just created

        cd json-forms

1.  Create a copy of the required virtual environment with
    this command (you should do this just once):

        conda env create -f environment.yml

2.  Activate the virtual environment (you should do this every
    time you start a new shell):

        conda activate pyqt

3.  Run the following command to exercise the test program:

        python src/jf/filler.py

You should then see a window that looks something like this.

[!img images/window.png]
