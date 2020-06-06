import csv

from string import Template

def replce(path,context):
    """
    Replaces the template variable in the text file with the context dict mapping

    Example:
    ```
    context = {'name': Bruce,'age':18}
    text = "Hello, my name is $name and I'm $age years old.

    returns "Hello, my name is bruce and I'm 18 years old."
    ```
    """
    with open(path,"r") as text:
        mailtext = text.read()

    s = Template(mailtext)
    return s.substitute(context)

def mapping(path):
    """
    maps the fields in csv file to the rows.
    Returns a list of dict where each dict has fieldname as key and corresponding row as value
    """
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
    return [ { k:v 
            for k,v in row.items() } 
            for row in reader ]

