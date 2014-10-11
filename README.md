# phone_directory

Twilio and Flask app for maintaining a database of users with their current phone numbers.


## Description

This application exposes HTTP endpoints that make it possible for someone to ensure that their phone number is up to date in the database. 

The flow looks like this:

1. Enter your id number
2. If your id number is correct: Enter your new phone number
3. Save phone number in the database
4. If your id number is incorrect, you can try again.


## Getting started

It can be quite confusing to get twilio up and running from scratch.  There are many tutorials to do this, but here is how we were the most successful.

1. Create a Twillio Account (http://www.twilio.com) you'll get a phone number from twilio, this will be important, and is super easy to do.
2. `pip install -r requirements.txt --use-mirrors` to install the required packages
3. Download and install [ngrok](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html) on OSX you can type `brew install ngrok` (if you have [homebrew](http://brew.sh/) installed)
4. Start ngrok and have it listen on port 5000 `ngrok 5000` you will get back a specific url like: http://6b405a6d.ngrok.com
5. Goto the Twillio Dashboard, click on "numbers", click on your twilio number, and for your voice url enter your ngrok server url, i.e. http://6b405a6d.ngrok.com/
6. Now you should be able to call your twilio phone number and try things out!


## Running tests

Type: ``` nosetests ``` in the root directory to run the test suite.


## TODO:

1. Get the basic app and menu working
2. update readme
3. add a real database backend
4. add more advance menu functionality
5. allow people to create accounts via phone, and receive SMS confirmation (this will require using the twilio Auth options, and be more advanced)


## Credits and Thanks

- Rachel Leventhal, executive director and founder, [Women's Peer to Peer Network](www.womensp2p.org)
- Our Hatian contributors, Anne, Carla, Josie Anne, Lusmat, Tabitha, and Rose, who wrote the [ivr-original](https://github.com/womensp2p/ivr-original) code in a 2012 internship. We initially set out to write a twilio app integrating with this code, but ran into problems running and integrating the code, so had to rewrite it in python.
- Professor Tayana Etienne, Science Department of the Haiti State University



