import datetime, time, os, smtplib
from sheet import MDASheet
from shifts_algo.placement import Placement
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

def create_MDA():
    start = time.time()
    load_dotenv()
    # get next month year and month
    if not os.getenv("SHIFTS_LINK") or not os.getenv("SENDER_ADDRESS") or not os.getenv("RECEIVER_MAIL") or not os.getenv("EMAIL_PASSWORD"):
        raise("you are missing some env")
    current_date = datetime.datetime.now()
    next_month_date = current_date + relativedelta(months=1)
    year: int = next_month_date.year
    month: int = next_month_date.month
    
    sheet = MDASheet()
    sheet.create_headers()
    sheet.create_sides(year, month)
    place_volunteers = Placement()
    year_month = f'{year}-{month:02}'
    place_volunteers.create_table_from_link(year_month, "1")
    place_volunteers.read_data()
    shifts = place_volunteers.assign_volunteers_to_shifts()
    shifts = place_volunteers.change_shifts_for_MDA_Modiin(shifts)
    sheet.fill_table(shifts)
    sheet.add_unsigned_to_table(shifts)
    sheet.display()
    print("Excel file created successfully!")
    send_email(year_month)
    print(f"the whole thing took {time.time()- start:.5f} seconds")
    
def send_email(month: str):
    subject = f"MDA shifts {month}"
    body = f"This is the shifts sheet for {month}"
    sender_email = os.getenv("SENDER_ADDRESS")
    recipient_email = os.getenv("RECEIVER_MAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    path_to_file = 'MDA_sheet.xlsx'

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    #attach file
    with open(path_to_file,'rb') as file:
        message.attach(MIMEApplication(file.read(), Name="MDAShifts.xlsx"))

    #for sending email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())


if __name__ == "__main__":
    create_MDA()
