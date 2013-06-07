Usage
============

You can use this app in two ways to protect the login view. 

* Use the provided deocrator (*antibrute_login*) to wrap your login view
* Use the methods in main module to check and record login attempts. Here are the useful methods.
 1. check_and_update_lock 
 2. get_lockout_response
 3. process_login_attempt
 
Here is a description of using the above functions when you get request for authenticating a user.
Read decorator function and main module for details about these functions.

* Check if provided user name is already locked.
* If locked then send the lockout response, otherwise proceed to check username/password combination.
* Process the login attempt to record failed/succeeded attempt (This will also check if lock needs to be applied). 


Configurations
=================

To override configuration variables in appsettings, prefix them with *ANTIBRUTE_* and assign new value in settings module.

__e.g. ANTIBRUTE_FORM_USER_FIELD = 'email'__

* You shuld confirm that FORM_USER_FIELD is correct in appsettings
* Read appsettings module to check what you can configure


#### Response after lockout ####
There are three options to return HttpResponse in case a user name is locked. These are checked in the following order.
1. *LOCKOUT_MSG_URL*: Redirect to a fixed URL that displays your message
2. *LOCKOUT_TEMPLATE*: Use this template to render the response. You get remaining seconds as context variable in this case.
3. *Plain HttpResponse*: If none of the above variables are set then a simple HttpResponse message is returned. 
