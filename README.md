#phone_directory

Twilio and Flask app for maintaining a database of users with their current phone numbers.


## details

This application exposes HTTP endpoints that make it possible for someone to ensure that their phone number is up to date in the database.

The flow looks like this:

1. Enter your id number
2. If your id number is correct: Enter your new phone number
3. Save phone number in the database
4. If your id number is incorrect, you can try again.

## Getting started

It can be quite confusing to get twillio up and running from scratch.  There are many tutorials to do this, but here is how we were the most successful.

1. Make sure you can run the flask app. (you will need a few basic python libraries to get started)
2. (pip, flask)
3. `python run.py`
4. Create a Twillio Account (http://www.twillio.com)
5. Download and install ngrok (https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html) on OSX you can type `brew install ngrok`

6. Goto Twillio
