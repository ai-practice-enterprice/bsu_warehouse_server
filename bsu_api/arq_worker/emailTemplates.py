from jinja2 import Environment, BaseLoader , Template
from enum import Enum
from datetime import datetime
import os
ender_email = "john.doe@blueskyunlimited.org"
receiver_email = "robot.one@blueskyunlimited.org"
# "robot.two@blueskyunlimited.org"
# "robot.three@blueskyunlimited.org"
# "robot.four@blueskyunlimited.org"
# "robot.five@blueskyunlimited.org"

# https://www.geeksforgeeks.org/email-templates-with-jinja-in-python/

class EmailType(Enum):
  WARNING = 0
  INFO = 1
  REQUEST = 2
  CONFIRMATION = 3


class JinjaEmailTemplateBuilder:
  def __init__(
      self, 
      email_type: EmailType = EmailType.INFO
    ):    
    self.email_type = email_type
    
    script_path = os.path.dirname(__file__)
    if self.email_type == EmailType.INFO: email_path = os.path.join(script_path,"email_templates","emailInfo.html")
    elif self.email_type == EmailType.WARNING: email_path = os.path.join(script_path,"email_templates","emailWarning.html")
    elif self.email_type == EmailType.REQUEST: email_path = os.path.join(script_path,"email_templates","emailInfo.html")
    elif self.email_type == EmailType.CONFIRMATION: email_path = os.path.join(script_path,"email_templates","emailConfirmation.html")
    else: email_path = os.path.join(script_path,"email_templates","emailInfo.html")
    
    with open(email_path, "r") as file:
      template_str = file.read()

    with open(os.path.join(script_path,"email_templates","general_email_style.txt"),"r") as file:
      self.css_str = file.read()


    self.jinja_template: Template = Template(template_str)

  def render(self, **kwargs):
    # see email_templates => .html files for info for arguments to the email template 
    
    robot_namespace = kwargs.get("robot_namespace", "/<ns...>")
    status = kwargs.get("status", "unknown")
    robot_message = kwargs.get("robot_message", "This is a sample email generated using Jinja2")

    if self.email_type == EmailType.INFO:
      email_data = {
        "subject": "Robot Info Notification",
        "header_title": "Robot Information",
        "robot_namespace": robot_namespace,
        "status": status,
        "message": robot_message,
        "year": str(datetime.now().year),
        "general_style": self.css_str,
      }

    elif self.email_type == EmailType.WARNING:
      email_data = {
        "subject": "Robot Warning Notification",
        "header_title": "Robot Warning",
        "robot_namespace": robot_namespace,
        "status": status,
        "message": robot_message,
        "year": str(datetime.now().year),
        "general_style": self.css_str,
      }
    
    elif self.email_type == EmailType.REQUEST:
      email_data = {
        "subject": "Robot Request Notification",
        "header_title": "Robot Request",
        "robot_namespace": robot_namespace,
        "status": status,
        "message": robot_message,
        "year": str(datetime.now().year),
        "general_style": self.css_str,
      }

    elif self.email_type == EmailType.CONFIRMATION:
      email_data = {
        "subject": "Robot Confirmation Notification",
        "header_title": "Robot Confirmation",
        "robot_namespace": robot_namespace,
        "status": status,
        "message": robot_message,
        "year": str(datetime.now().year),
        "general_style": self.css_str,
      }


    else:
      email_data = {}
      
    email_content = self.jinja_template.render(email_data)
    return email_content
  