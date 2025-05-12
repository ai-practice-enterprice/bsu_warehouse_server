from jinja2 import Environment, BaseLoader , Template
from enum import Enum
from datetime import datetime

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


class JinjaEmailTemplateBuilder:
  def __init__(
      self, 
      email_type: EmailType = EmailType.INFO
    ):    
    self.email_type = email_type
    
    if self.email_type == EmailType.INFO:
      with open("email_templates/emailInfo.html", "r") as file:
          template_str = file.read()

    self.jinja_template: Template = Template(template_str)

  def render(self, **kwargs):
    # see email_templates => .html files for info for arguments to the email template 
    
    if self.email_type == EmailType.INFO:
      robot_namespace = kwargs.get("robot_namespace", "/<ns...>")
      status = kwargs.get("status", "unknown")
      robot_message = kwargs.get("robot_message", "This is a sample email generated using Jinja2")
      email_data = {
        "subject": "Greetings from robot",
        "header_title": "Info",
        "robot_namespace": f"Hello {robot_namespace}!",
        "status": f"{status}",
        "message": f"{robot_message}",
        "year": str(datetime.now().year),
      }
    elif self.email_type == EmailType.WARNING:
      pass

    elif self.email_type == EmailType.REQUEST:
      pass

    else:
      email_data = {}
      
    email_content = self.jinja_template.render(email_data)
    return email_content
  