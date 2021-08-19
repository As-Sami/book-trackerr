# BooK-TrackeR

A discord bot to track pdfs your book.    

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Steps for hosting a bot for your own server using Heroku.

1. To set it on heroku, you'll need an acoount in heroku. Make an account and download the CLI from [here](https://devcenter.heroku.com/articles/heroku-cli)

2. Open up terminal or Command Prompt and enter the command `heroku login`. It will take you to the browser to login. 

3. Now clone this repository using the command `git clone https://github.com/As-Sami/book-trackerr.git`

4. After cloning move to the book-trackerr folder using this command `cd book-trackerr`

5. Now enter `heroku create` command in the terminal and hit enter. It will create a new app for you. Remember the name.

6. Now you need to add the Python buildpack to install essential packages.

7. To add Python buildpack type the following command `heroku buildpacks:add heroku/python`.

8. Now go to the personal dashboard [page](https://dashboard.heroku.com/apps) 
of heroku on your browser.

9. Next click on the app you created in step 6.

10. Now, go to resources and click on Find more add-ons and find Heroku Postgres.

11. Click to install the database on the Hobby Dev plan and set the app to the one that hosts the bot.

12. Go to settings tab and you will see a section called Config Vars. Click on the reveal config vars button.

13. Now you need to create a config var called **BOT_TOKEN** and paste your bot token created using discord and hit add. You need to add another variable and that is the id for super users (read the description below to know about super user). Create a config val named **SUPER_USERS** and put ids with a comma at middle. (Example: `12345` or `12345,6789,343534`). 

14. Make sure that the name of the config var that contains the database url is named **DATABASE_URL**.

15. Now the setup is almost done. Type the following command `git push heroku master -f` and press enter.

16. It will take few minutes to build and deploy.

17. After successful build open the heroku app in your browser. The same step as 8.

18. Go to Resources tab and turn on the worker. You are not charged for doing this its completely free.

19. Enjoy..................................................


## Config Vars

**BOT_TOKEN** : the Discord Bot Token for your bot.
**SUPER_USERS** : ids of super users. Super users are those people who can use the add and delete command. To get their id, go to the setting of your discord and then go to Advance and turn on developer mode. Now the person you want to make super user, right click on his profile and you will see a copy `COPY ID`. Just click on the copy `COPY ID` button and you will get the id.
