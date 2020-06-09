# Pymailer
Python script that sends emails based on a template text from a csv file.

## Requirements

* You need a csv file named `database.csv` with at least `email` as fieldname.
* A text file `mailtext.txt` that will contain your template message.
* A python file `secret.py` with your email and password as shown in [`secret_sample.py`](../master/example/secret_sample.py)

**Note**: If you have a Gmail account, you don't need to provide your password in the file.

## Usage

This script

## Provider

### **Gmail**

If you're a gmail user, you will need to create an application in google projects, this will use OAuth for added security.

You can follow the steps here, the wizard link is [here](https://console.developers.google.com/start/api?id=gmail). After you download the file, rename it to `credentials.json`

**Note**: You only need to do this once.


![Imgur](https://i.imgur.com/cllmO33.jpg)


### **Other**

If your provider offers an SMTP address, you should provide your mail and password in the python file `secret.py`.

### Example

Suppose we have a csv like this

|name|email|company|
|-----|-----|-------|
|John|mail@company.com|Python Company|

__Template Mail__ :
```
Hello $name

I hope I can work in your company $company
Thanks
```

The email sent to `mail@company.com` will be:
```
Hello John.

I hope I can work in your company Python Company.
Thanks
```
The script will iterate on every entry of the csv file.

## **Important** :
The template variables should be prefixed with `$` and refer to a fieldname in the csv file.
-------
You can run an example (since the example uses the file [`secret_sample.py`](../blob/master/example/secret_sample.py), you should change the `user_mail` and `password` with your own credentials) with
```
python example.py
```

# **Run**

To run the script :
```
python main.py
```
