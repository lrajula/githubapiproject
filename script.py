import datetime, requests, smtplib, xlsxwriter, time, os, logging, sys
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders




# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger(__name__)


# Replace {GITHUB_TOKEN}, {GITHUB_USERNAME} and {GITHUB_REPO} with your GitHub repository details
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_REPO = os.environ.get('GITHUB_REPO')

# Email configuration


sender_email = os.environ.get('SENDER_EMAIL')
receiver_email = os.environ.get('RECEIVER_EMAIL')
smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')
smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')


# Get the date range for the past week
today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)
last_week_str = last_week.strftime("%d-%m-%Y")




# Construct the API URL for pull requests
api_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/pulls?state=all&sort=created&direction=desc'

"""
state string
Either open, closed, or all to filter by state.

Default: open

Can be one of: open, closed, all
"""

def process_pull_requests():

    # Send the GET request to the GitHub API
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    try:
        response = requests.get(api_url, headers=headers)
        logger.info("github api request has been processed")
    except requests.exceptions.RequestException as err:
        logging.error ("Failed to connect GitHubAPI, Please check Error ",err)
        sys.exit(1)

    if not response.json():
        logger.info("No Pull Request in mentioned repo %s" %(GITHUB_REPO))
        send_email("No Pull Request Found in the given repo " + GITHUB_REPO, "No Pull Request Found in the given repo", 0, "")
        

    if response.status_code == 200:
        pull_requests = response.json()
        opened_prs = []
        closed_prs = []
        opned_pr_info_ls = []
        closed_pr_info_ls = []


        for pr in pull_requests:
            
            pr_date = datetime.datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
            if last_week <= pr_date <= today:
                if pr['state'] == 'open':
                    opened_prs.append(pr)
                    open_pull_request_info = "\n".join([f"Title: {pr['title']}\nURL: {pr['html_url']}\n"])
                    logger.info("open_pull_request_info %s \n" %(open_pull_request_info))
                    opned_pr_info_ls.append(open_pull_request_info)
                elif pr['state'] == 'closed':
                    closed_prs.append(pr)
                    closed_pull_request_info = "\n".join([f"Title: {pr['title']}\nURL: {pr['html_url']}\n"])
                    logger.info("closed_pull_request_info %s \n" %(closed_pull_request_info))
                    closed_pr_info_ls.append(closed_pull_request_info)
                
        
        if not len(opened_prs) and len(closed_prs):
            logger.info("No Pull Request in mentioned repo %s" %(GITHUB_REPO))
            send_email("No Pull Request Found in Last Week " + GITHUB_REPO, "No Pull Request Found in Last Week", 0, "")
            

        # Call the function to add data to the Excel file
        sheetname = last_week_str 
        try:
            workbook_name = add_data_to_xlsxwriter(sheetname, len(opened_prs), opned_pr_info_ls, len(closed_prs), closed_pr_info_ls)
        except Exception as err:
            logger.error("ERROR While Processing Data add_data_to_xlsxwriter", err)
            sys.exit(1)
        email_subject = "Pull request Summary Since Last Week " + last_week_str
        email_body = "Open PR's - %s \n Closed PR's - %s \n Please find the attached excel sheet for more information" % (str(len(opened_prs)), str(len(closed_prs)))
        send_email(email_subject, email_body, opened_prs, workbook_name)



def add_data_to_xlsxwriter(sheetname, opened_prs, opned_pr_info_ls, closed_prs, closed_pr_info_ls):

    # Create a workbook and add a worksheet.
    workbook_name = 'GitHub PR Summary '+sheetname+'.xlsx'
    workbook = xlsxwriter.Workbook(workbook_name)
    worksheet = workbook.add_worksheet(sheetname)

    # # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    
    # Adjust the column width.
    worksheet.set_column(1, 1, 50)

    # Write some data headers.
    worksheet.write('A1', 'Open PR', bold)
    worksheet.write('B1', 'Open PR Info', bold)
    worksheet.write('C1', 'Closed PR', bold)
    worksheet.write('D1', 'Closed PR Info', bold)

    prs = (
        [str(opened_prs), str(opned_pr_info_ls), str(closed_prs), str(closed_pr_info_ls)],
    )

    # Start from the first cell below the headers.
    row = 1
    col = 0

    for opened_prs, opned_pr_info_ls, closed_prs, closed_pr_info_ls in (prs):

        worksheet.write_string (row, col,  opened_prs)
        worksheet.write_string(row, col + 1, opned_pr_info_ls )
        worksheet.write_string(row, col + 2, closed_prs )
        worksheet.write_string(row, col + 3,  closed_pr_info_ls)
        row += 1

    workbook.close()
    return workbook_name


def send_email(subject, body, opened_prs, workbook_name):

    if not opened_prs and workbook_name == "":

        # Compose the email
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                logger.info("Email sent successfully!")
                server.close()
        
        except smtplib.SMTPException as e:
            logger.error("Error: unable to send email %s", e)

    if opened_prs and workbook_name != "":

        # Compose the email
        message = MIMEMultipart()
        message.attach(MIMEText(body, 'plain'))
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Logging info summary report
        logger.info("From: %s" %(sender_email))
        logger.info("To: %s" %(receiver_email))
        logger.info("Subject: %s \n" %(subject))
        

        # open the file to be sent 
        filename = workbook_name
        attachment = open(filename, "rb")
        
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        
        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        message.attach(p)

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                logger.info("Email sent successfully!")
                server.close()
        
        except smtplib.SMTPException as e:
            logger.info ("Error: unable to send email %s", e)



# Run the script at regular intervals
interval = 15  # 1 hour
while True:
    process_pull_requests()
    time.sleep(interval)
