# ig_tagger
Python script that automates the process of tagging people in Instagram giveaways.

# How it works
Before trying to run the script you must first open config.ini file with a text editor and input:

1. The contest url
2. The list of names to tag
3. The number of tags per comment
4. Your IG username and password (these are used to log you in your account automatically)

When running the script a Chrome window will open with the message "Chrome is being controlled by automated test software". Instagram's login page will appear and you'll be loged into your account. After that you'll be redirected to the contest page, that you provided. The script now is going to choose as many random names as the number you entered in step 3 mentioned above. Names can be repeated between different comments, so make sure to read the giveaway's rules carefully.

After each comment, the script selects a random number of seconds to wait before commenting again. This way it minimizes the potential of IG algorithm blocking you. If, however, you get blocked it waits for 1 minute before trying to comment again. This process is repeated until IG's block disappears.

You can stop the script by pressing CTRL + C on the terminal (Linux environment) and it will output the total number of comments it made.

# Requirements
You must have Python3 and pip installed on your system (tested with Python 3.7.5 and 3.8.3). Then run ``` pip install selenium ```.

**Strongly Recommended** 
Create a virtual environment by typing `python3 -m venv ./yourname`. Activate the environment by typing `source ./yourname/bin/activate` and finally install selenium package inside the virtual environment like mentioned above.

To run this script you need to navigate inside it's directory and type ``` python ig_tagger.py ```.

If you get an error about Chrome and chromedriver incompatible version, then open Chrome and navigate to chrome://version. Locate the version of your browser and download the appropriate chromedriver from [here](https://chromedriver.chromium.org/downloads). Replace the project's chromedriver with the chromedriver you just downloaded and you're done.
