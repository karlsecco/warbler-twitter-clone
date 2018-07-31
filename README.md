# Warbler

## Description

- Twitter-like online social networking platform allowing users to post/view/like messages and follow other users
- CSRF form secured app using Python, Flask, and SQLAlchemy to manage PostgreSQL relational database; deployed to Heroku

## Demo

- Live application: [http://at-warbler.herokuapp.com/](http://at-warbler.herokuapp.com/)

## Project notes

Updates as of 3/25/18:

* Unique message like/unlike feature and liked messages display page for each user
* Unique username and ability to display/edit personal information and profile images
* Forms and form submit button features--follow/unfollow, like/unlike, delete message, delete user, search--secured via CSRF token validation
* Search method changed to POST to hide CSRF token from query string
* Follow button removed from user's profile page, disallowing signed in user to follow his/her own account
* Conditional jinja logic added to display updated user info/images; static folder routes will no longer be displayed 
* Variable/route naming syntax for follwer/follwee corrected site-wide
* Home page now displays top 100 most recent messages from followed accounts and signed in user, else top 100 most recent posts if user is following no one
* All users' header images displayed upon search instead of initial default image setting
* 'data.sql' seed file adjusted to remove broken images
* 404 error page added including site-wide nav header to help redirect users appropriately

## Notes about the author

Karl Secco is a full stack software engineer proficient in React Native, React, Redux, and JavaScript, passionate about creating clean, maintainable code and streamlined user experiences. A graduate of [Rithm School](https://www.rithmschool.com/), Karl most recently fulfilled a React Native (iOS) contract for [Groupmuse](https://www.groupmuse.com/). For more information, please visit [www.karlsecco.com](http://www.karlsecco.com)
