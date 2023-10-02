# Postfix Server Email Filtering using Python

Python program that assist on filtering email before queue in Postfix server using purepythonmilter library. 

# Instruction

This instruction will guide the user from installing the necessary tools and library through the usage of the program

The prerequisite of this program that it is required to be performed on Ubuntu OS

## Postfix Installation

1. Install the ```postfix``` package if it has not been installed

```
sudo apt-get install postfix
```

Here below are the configuration for the postfix installation


    General type of mail configuration?: Internet Site
    System mail name: example.com (not mail.example.com)
    Root and postmaster mail recipient: The username of your primary Ubuntu account (example: jake)
    Other destinations to accept mail for: $myhostname, example.com, mail.example.com, localhost.example.com, localhost
    Force synchronous updates on mail queue?: No
    Local networks: 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
    Mailbox size limit: 0
    Local address extension character: +
    Internet protocols to use: all

2. Install the ```mailutils``` package

```
sudo apt-get install mailutils
```

## Python Installation

1. Install the ```python3``` package

```
sudo apt-get install python3
```

2. Install the ```pip``` package

```
sudo apt-get install python3-pip
```

3. Install the ```purepythonmilter``` package

```
pip install purepythonmilter
```

## Setup the Postfix Server

The example of ```main.cf``` can be seen in the  

1. Configure Postfix to use Maildir-style mailboxes

```
sudo postconf -e "home_mailbox = Maildir/"
```

2. Open Postfix ```main.cf`` file

```
sudo nano /etc/postfix/main.cf
```

3. Go to the bottom of the file and add this line of text

```
smtpd_milters = inet:127.0.0.1:9000
```

the line indicates the IP adress and the port which can be change based on the user

4. Save the file by Ctrl+X and Press Y (indicates that you wanted to save the changes) 

## Testing the Postfix Server

To test whether the postfix server able to receive mail, it is required to create other user that act as the sender of the mail

1. To create the user, start with command below

```
sudo useradd -m -s /bin/bash testuser
```

'testuser' can be replaced with any name and act as indication for the user that sends the mail

2. Create password for the sender

```
sudo passwd testuser
```

3. Make the sender as the super user

```
sudo usermod -aG sudo testuser
```

4. Login to the sender account

```
su - testuser
```

5. Initialize the Postfix server

```
sudo postfix start
```

6. Create connection through localhost

```
telnet localhost 25
```

7. Create a mail that will be sent by the sender to the recepient

```
ehlo localhost
mail from: testuser@localhost
rcpt to: root@localhost
data
Subject: Test Subject

Test Body
.
quit
```

The 'testuser' and 'root' represent the sender and the recepient, therefore the naming can be adjusted based on what is initially defined in your machine and step 1

8. Logout from the sender account and check the incoming mail in the receiver

```
logout
```

```
mail
```

If you see new mail, therefore its indicates success on the sending messages

## Testing Python Filtering System 

To test the python filtering system, it is required to run the python program first before running the postfix. Before running the program, it is required to check if the IP address and the port variable inside the python program matches with the IP address and port ```smtpd_milters``` in the ```main.cf``` files

1. Type command below to run python

```
python3 filterBeforeQueue.py
```

Once the python program runs, it its required to perform steps 4 to 6 from the ```Testing the Postfix server``` Section

2. To test whether the filtering system works, it is required to send email that will be rejected based on the criteria of the python filter (in this example, filtering all email comes from example.com)

```
ehlo localhost
mail from: testuser@example.com
```

If the terminal display warning, it indicates that the filtering system is working

The restriction rules can be adjusted in the python file by accessing the isSpam function, which indicates what are the rules that classify whether the mail is a spam or not