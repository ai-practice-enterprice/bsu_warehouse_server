# sending a email to the mail server first when the server gets a message over the topic
# https://realpython.com/python-send-email/
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "john.doe@blueskyunlimited.org"
receiver_email = "robot.one@blueskyunlimited.org"
# "robot.two@blueskyunlimited.org"
# "robot.three@blueskyunlimited.org"
# "robot.four@blueskyunlimited.org"
# "robot.five@blueskyunlimited.org"

password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "warning robot"
message["From"] = sender_email
message["To"] = receiver_email

warning_notification = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>ROS2 Robot Notification</title>
  <style>
    body {
      font-family: "Segoe UI", Roboto, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }
    .container {
      background-color: #ffffff;
      max-width: 600px;
      margin: 30px auto;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .header {
      background-color: #005dab;
      color: white;
      padding: 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
    }
    .content {
      padding: 30px;
      color: #333333;
    }
    .content h2 {
      color: #005dab;
    }
    .status {
      background-color: #e6f4ff;
      border-left: 4px solid #005dab;
      padding: 15px;
      margin: 20px 0;
      border-radius: 5px;
      font-family: monospace;
    }
    .footer {
      text-align: center;
      font-size: 12px;
      color: #888;
      padding: 20px;
    }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>🤖 ROS2 Robot Alert</h1>
  </div>
  <div class="content">
    <h2>Status Update: Robot "Alpha-1"</h2>
    <p>Dear Operator,</p>
    <p>Here is the latest system report from your ROS2 robot:</p>
    
    <div class="status">
      Node: <strong>navigation_stack</strong><br>
      Status: <span style="color:green;">ACTIVE</span><br>
      Battery: <span style="color:orange;">78%</span><br>
      Last Seen: 2025-05-08 10:24 UTC<br>
      Location: Zone B-7
    </div>

    <p>If any parameter exceeds the threshold, an alert will be triggered immediately.</p>

    <p>Thank you for using the ROS2 Monitoring Service.</p>

    <p> ROS2 Notification System</p>
  </div>
  <div class="footer">
    &copy; 2025 RobotOps Inc. | ROS2 Monitoring System
  </div>
</div>

</body>
</html>
"""
part1 = MIMEText(warning_notification, "html")
message.attach(part1)
context = ssl.create_default_context()
with smtplib.SMTP_SSL("#BSU email server name (DNS record)", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )