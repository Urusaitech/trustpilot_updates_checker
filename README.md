# trustpilot_updates_checker
Check if the amount of reviews changes for a given company. If so, sends message to your telegram.  
  
_Linted with flake8 and black_

# How to run
 
- download/clone project to your IDE
- install python 3+ interpreter 
- install requirements using prompt: **pip install -r requirements.txt** 
- create file configs.py and put your telegram user id, bot token, and url of the target company inside it
- run main.py

## Logging

Script saves results of its work to trust_log.log


# Example of configs.py

![image](https://user-images.githubusercontent.com/100962655/221352731-072b02a4-aa45-4bf7-9c8f-1c8a3458a8e8.png)
  
**update_reviews_txt** = _bool_  # use True at the first start  
**tg_notify** = _bool_  # choose whether to send notification in TG or not  
**timeout** = _int_  # set high border of time between checks in seconds  
**token** = _str_  # token of your telegram bot, you can create one using Father Bot  
**chat_id** = _int_  # id of your TG username. Note: bot can't send you a message until you write him something first  
**url** = _str_  # link to a tracked company, use 'sorted by recency' for a more accurate tracking
