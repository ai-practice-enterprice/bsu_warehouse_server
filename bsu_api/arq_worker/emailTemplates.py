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

class MessageType(Enum):
  WARNING = 0
  INFO = 1
  REQUEST = 2
  CONFIRMATION = 3

class TemplateType(Enum):
  EMAIL = 1
  NOTIFICATION = 2


class JinjaEmailTemplateBuilder:
  def __init__(
      self, 
      message_type: MessageType = MessageType.INFO
    ):    
    self.message_type = message_type
    self.script_path = os.path.dirname(__file__)
    
  def build_email(self, **kwargs):
    if self.message_type == MessageType.INFO: email_path = os.path.join(self.script_path,"email_templates","emailInfo.html")
    elif self.message_type == MessageType.WARNING: email_path = os.path.join(self.script_path,"email_templates","emailWarning.html")
    elif self.message_type == MessageType.REQUEST: email_path = os.path.join(self.script_path,"email_templates","emailInfo.html")
    elif self.message_type == MessageType.CONFIRMATION: email_path = os.path.join(self.script_path,"email_templates","emailConfirmation.html")
    else: email_path = os.path.join(self.script_path,"email_templates","emailInfo.html")
    
    with open(email_path, "r") as file:
      template_str = file.read()

    with open(os.path.join(self.script_path,"email_templates","general_email_style.txt"),"r") as file:
      self.css_str = file.read()

    self.template_type = TemplateType.EMAIL
    self.jinja_template: Template = Template(template_str)

    self.robot_namespace = kwargs.get("robot_namespace", "/<ns...>")
    self.status = kwargs.get("status", "unknown")
    self.robot_message = kwargs.get("robot_message", "This is a sample email generated using Jinja2")

  def build_frontend_notification(self, **kwargs):
    if self.message_type == MessageType.INFO: email_path = os.path.join(self.script_path,"notification_templates","notification_info.html")
    elif self.message_type == MessageType.WARNING: email_path = os.path.join(self.script_path,"notification_templates","notification_warning.html")
    elif self.message_type == MessageType.REQUEST: email_path = os.path.join(self.script_path,"notification_templates","notification_info.html")
    elif self.message_type == MessageType.CONFIRMATION: email_path = os.path.join(self.script_path,"notification_templates","notification_confirmation.html")
    else: email_path = os.path.join(self.script_path,"notification_templates","notification_info.html")
    
    with open(email_path, "r") as file:
      template_str = file.read()

    self.template_type = TemplateType.NOTIFICATION
    self.jinja_template: Template = Template(template_str)

    self.robot_namespace = kwargs.get("robot_namespace", "/<ns...>")
    self.status = kwargs.get("status", "unknown")
    self.robot_message = kwargs.get("robot_message", "This is a sample email generated using Jinja2")

  def render(self, **kwargs):
    # see email_templates => .html files for info for arguments to the email template 
    # see notification_templates => .html files for info for arguments to the email template 
    
    if self.message_type == MessageType.INFO:
      subject = "Robot Info Notification"
      header_title = "Robot Information"

    elif self.message_type == MessageType.WARNING:
      subject = "Robot Warning Notification"
      header_title = "Robot Warning"

    elif self.message_type == MessageType.REQUEST:
      subject = "Robot Request Notification"
      header_title = "Robot Request"

    elif self.message_type == MessageType.CONFIRMATION:
      subject = "Robot Confirmation Notification"
      header_title = "Robot Confirmation"

    else:
      email_data = {}

    email_data = {
        "subject": subject,
        "header_title": header_title,
        "robot_namespace": self.robot_namespace,
        "status": self.status,
        "message": self.robot_message,
        "year": str(datetime.now().year),
    }

    if self.template_type == TemplateType.EMAIL:
      email_data["general_style"] = self.css_str

    email_content = self.jinja_template.render(email_data)
    return email_content
  