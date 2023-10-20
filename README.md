# Postfix Server Email Filtering

This repository display 3 method to filtering email for postfix server (milter, before queue and after queue)

The milter is run through python program that assist on filtering email in Postfix server using purepythonmilter library. 

The after queue is run by assigning the shell script to master.cf, which is configuration file for postfix server.

To run each method of filtering, it is required to perform instruction until Testing the Postfix server

Below are the instructions to setup the postfix configuration and simulate email sending and the 3 methods of filtering system

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

The example of ```main.cf``` setting can be seen in the directory inside `/milter`  

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

To test the python filtering system, it is required to run the python program first before running the postfix. It is also required to check if the IP address and the port variable inside the python program matches with the IP address and port ```smtpd_milters``` in the ```main.cf``` files

1. Type command below to run python

```
python3 pythonMilter.py
```

Once the python program runs, it its required to perform steps 4 to 6 from the ```Testing the Postfix server``` Section

2. To test whether the filtering system works, it is required to send email that will be rejected based on the criteria of the python filter (in this example, filtering all email comes from example.com)

```
ehlo localhost
mail from: testuser@example.com
```

If the terminal display warning, it indicates that the filtering system is working

The restriction rules can be adjusted in the python file by accessing the isSpam function, which indicates what are the rules that classify whether the mail is a spam or not

## Setup Before Queue Filtering

## Testing Before Queue Filtering

## Setup After Queue Filtering

These steps can only be performed once Testing Postfix Server instruction has been completed

1. Open the script file afterQueue.sh to see the code and the filtering system

2. Make sure that the INSPECT_DIR is the directory of your postfix filter

3. To implement or modify the filtering system, place any code under the cat > in.$$

In this example the filtering section will reject if the domain of the sender is @example.com

4. Change the permission of your postfix filter directory to allow writing by others

```
chmod 777 /var/spool/filter
```

change the /var/spool/filter based on your postfix filter directory

5. Test the shell script manually by run the command below

```
./afterQueue.sh -f sender receiver < message.txt
```

replace sender with the email of the sender and receiver with the email of the receiver

make sure the sender email followed the filtering system that is setup based on the script (In this case @example.com is not accepted, therefore use any email that ends with @example.com sender) 

6. If the echo command executed therefore it indicates that the filtering system is working (In this case print out log of "Message is not accepted") 

If it does not work, recheck the permission on the filter directory and enable it to allow writing by others

7. Go to terminal and create new user called "filter" using this command

```
sudo useradd filter
```

The name "filter" can be exchanged to anything else

8. Open ```master.cf``` and write this section inside to link the shell script to Postfix After Queue Filter

```
# ==========================================================================
# service type  private unpriv  chroot  wakeup  maxproc command + args
#               (yes)   (yes)   (no)    (never) (100)
# ==========================================================================
filter    unix  -       n       n       -       10      pipe
    flags=Rq user=filter null_sender=
    argv=/path/to/afterQueue.sh -f ${sender} -- ${recipient}

smtp      inet  n       -       n       -       100      smtpd
        -o content_filter=filter:dummy
```

The user is based on the name of the user that is created on the previous step, and the /path/to/afterQueue.sh indicates the path to the afterQueue.sh script

to check the path run ```pwd``` on the selected directory that has afterQueue.sh

Make sure to replace the previous setting of the ```master.cf``` with this one to enable the after queue to run

9. Run ```sudo postfix reload``` to save the configuration

## Testing After Queue Filtering

1. To test whether the filtering system works, repeat the step 6 to 7 from the section of Testing the Postfix Server

Instead sending mail from testuser@localhost, replace the domain of the sender based on the filtered logic implemented (In the case @example.com supposed to be filtered, therefore replace to testuser@example.com)

2. To check the rejected mail, keep at the testuser terminal and run ```mail``` or ```mailq```, it will display the rejected mail and display the error based on setting in the script