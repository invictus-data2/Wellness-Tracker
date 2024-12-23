from django.shortcuts import render, redirect
from .forms import PreForm, PostForm
from .models import PreSessionMetrics, PostSessionMetrics
from datetime import datetime
from django.templatetags.static import static
import pywhatkit as kit
import matplotlib.pyplot as plt
import os
from .utils import get_client_names, get_coach_names
from threading import Thread

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [  'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
credentials_json= {
    "type": "service_account",
    "project_id": "automation-422503",
    "private_key_id": "5dc333faf9c1b06fe534dd748fb1d87567f7cfa3",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCd1aYmqrNNJvqs\nsjtf6vmPXM8312sq+fGCdq2p90exXhkOMg+83exW0diz8UZ7IPOqw4mWpmYXPytB\naMSBzScRO9UaSy+KdzxiVtSsKupXulWstKQRrkfARCAPOA1a1s8h5PM/PpkvQZeY\n9RT7+un5N8q8s2s13kF+EP6wfE0VJHI7gGvOeRBZGas9cCgHKbIE0nUwhZnI14V7\nqtI4oujtdbPA/jtDqs7N/xephFCCuV5gBEsfw1Ju2XdP0btr1vquLhELrfUK6gWD\na4xKkMV8YO9GhoMfgwl2WExFhOufQSpv5xokzHSb7J/mlejecujAhO1MuERHCdXM\nn9N3aHxrAgMBAAECggEARJLR9MO+Ufto9sYbANHsqkpG53qK36mnMakRS6KZfeil\nlyLN7p82swPKFGfz2MQYyazZ5t+VxGzYBLuZgNGasySdMibPWWfzjsAt9z1QAlx9\nI6N6Ewp2twSCL0qJltl0NcQsoOI4GK11SWnVu6Koq/P++9wx7L4LE1Qb656duNyl\nZDZ6W1e67lZ4Y9Ef4vA/sKJaoU554UzuhmdVj8CAJGa7ZPT/XtzVkSYnqFuoLNBk\nRwwo+DAutsfcBbCq9R4ymD23LO1KJMTDEQMzJKXJ9czbRtxTrNUZRBDL5SJAZ4Nk\nu+6HLxf9xIaqlyE0zFsZfyGUKwSssS76xzfgUMBT/QKBgQDVDlo236mLk/MnAB00\n9NFqsXmMbLysfH/nomGxZe4ciCv+OcvpTA/jFDNInmsXrhM8uGReCRaQCWWU6fF6\nm+dXYHg+cK2KB20NsVa9mfaHHP4I2w23iAHBicRwEWeucSaWpWwSNnWxDF7ootfY\nt8sDf/C4lduepw/+bEB530N3HQKBgQC9peEMfUF+JK3Da4AvWZrWIwH+HdTY2ugl\nQaXXgbZAWwfRNrB0Mk3qQ9EPpre9IFQbgEk0frg907lwaE5pbPoupfTxhgtazqHK\nmnULLnKUZoI6VpASen06zhf537dSwE0BK5ewK6noYMQWN+0Dhv9zDIDhyDqk4UQF\nOAZYV+wDJwKBgEoXhqoEmAqRNgL/GCkdZmJrO7Do86gsV7KvFrhBkU/czyfG47HL\nIM9AbCE57lY61DfOjCDjmjQXAHuL681OwGHzi31zY/ZXZMZZQKgJDeGo5HMh8qA7\nrRioF2c9tkfE072Z435l8AHVIoBWeSfFqtUZvhYDD3AZ+wbokHeRe/3FAoGAWUlq\nrh2eowwTvyiynhhavKyYuJJE7qAJodjJgq/wJVZ2VLqh0uMIKd4p5GuCoAlDb/sy\n/AMZLQqsiM6i9CG5nBLIQpnwaJ1WMPQNXOlOSq4EbADrLbf7k58KTLtWLSCaYI2s\nieXUxbIhP7Cu5vU8+WaOmz5Q1eW0x5w76IXkeQsCgYEAtWv74A5+9w6nTptmltDg\n+t2BTChHPbNbIvfmcr34bhjt95JWuos40Xg/Tjqla6+1/JVC60uJpnnmlPKVIX4O\nfRaDEfX4VmcrlvDMH4FDTGMFUO18eas2CmymRtdHSXVFEycB8S+kV1mZrmWXh4fR\nfXhC5gEYwKpAauDjHdRYm/0=\n-----END PRIVATE KEY-----\n",
    "client_email": "dataadmin@automation-422503.iam.gserviceaccount.com",
    "client_id": "116524974662221993471",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dataadmin%40automation-422503.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
client = gspread.authorize(credentials)
sheet = client.open("Wellness").worksheet("pre_Session")
sheet1 = client.open("Wellness").worksheet("post_Session")
coach_directory = client.open("Wellness").worksheet("coach_Directory")

def index(request): 
    return render(request, 'home.html')  

def success_pre_view(request):
    return render(request, 'success_pre.html')  # Ensure this template exists

def success_post_view(request):
    return render(request, 'success_post.html')  # Ensure this template exists

def get_coach_number(coach_name, country_code="+91"):
    """
    Fetch the phone number of the coach from the coach_Directory worksheet.
    """
    try:
        records = coach_directory.get_all_records()
        for record in records:
            if record['Coach Name'] == coach_name:
                return f"{country_code}{record['Mobile Number']}"
        return None
    except Exception as e:
        print(f"Error fetching coach number: {e}")
        return None

# Pre-Session View
def pre_session_view(request):
    client_names = get_client_names()
    coach_names = get_coach_names()
    if request.method == 'POST':
        form = PreForm(request.POST)
        if form.is_valid():
            # Extract values from the form
            client_name = form.cleaned_data['client_name']
            coach_name = form.cleaned_data['coach_name']
            date = form.cleaned_data['date']
            weight = form.cleaned_data['weight']
            sleep = form.cleaned_data['sleep']
            soreness = form.cleaned_data['soreness']
            mental_stress = form.cleaned_data['mental_stress']
            fatigue = form.cleaned_data['fatigue']
            pain_scale = form.cleaned_data['pain_scale']
            stiffness = form.cleaned_data['stiffness']
            grip_strength = form.cleaned_data['grip_strength']
            rhr = form.cleaned_data['rhr']
            sleep_quantity = form.cleaned_data['sleep_quantity']

           
            # Weights for each metric (adjust these weights based on your needs)
            w_sleep = 0.35
            w_sore = 0.075
            w_stress = 0.075
            w_fatigue = 0.075
            w_pain = 0.35
            w_stiffness = 0.075

            # Calculate the composite score
            composite_score = (
                (w_sleep * (sleep*2)) +
                (w_sore * (10 - (soreness*2))) +
                (w_stress * (10 - (mental_stress*2))) +
                (w_fatigue * (10 - (fatigue*2))) +
                (w_pain * (10 - (pain_scale*2))) +
                (w_stiffness * (10 - (stiffness*2)))
            ) * 10

            # Create and save the model instance
            pre_session_metrics = form.save(commit=False)
            pre_session_metrics.composite_score = composite_score
            pre_session_metrics.save()  # Save to the database

            # Prepare data for Google Sheets (make sure `sheet` is defined elsewhere in your project)
            data = [
                client_name,
                coach_name,
                date.strftime('%Y-%m-%d'),  # Format the date
                weight,
                sleep,
                soreness,
                mental_stress,
                fatigue,
                pain_scale,
                stiffness,
                composite_score,
                grip_strength,
                rhr,
                sleep_quantity
            ]

            # Append data to Google Sheets
            sheet.append_row(data)  # Ensure this function is properly defined in your project

            # Function to format each metric based on thresholds
            def format_metric(value, threshold, emoji, is_less_than_or_equal=True):
                alert = "⚠️"  # A red block emoji to indicate color
                formatted_value = f"{value}/5"
                
                if is_less_than_or_equal:
                    if value <= threshold:
                        # Mark both the key and value in dark red
                        return f"*{emoji}*: *{formatted_value}* {alert}"
                    else:
                        return f"{emoji}: {formatted_value}"  # Regular for values > threshold
                else:
                    if value >= threshold:
                        # Mark both the key and value in dark red
                        return f"*{emoji}*: *{formatted_value}* {alert}"
                    else:
                        return f"{emoji}: {formatted_value}"  # Regular for values < threshold


            # Format each metric using the function
            sleep_metric = format_metric(sleep, 3, "Sleep", is_less_than_or_equal=True)
            soreness_metric = format_metric(soreness, 3, "Soreness", is_less_than_or_equal=False)
            mental_stress_metric = format_metric(mental_stress, 3, "Mental Stress", is_less_than_or_equal=False)
            fatigue_metric = format_metric(fatigue, 3, "Fatigue", is_less_than_or_equal=False)
            pain_scale_metric = format_metric(pain_scale, 3, "Pain Scale", is_less_than_or_equal=False)
            stiffness_metric = format_metric(stiffness, 3, "Stiffness", is_less_than_or_equal=False)
            grip_strength_metric = f"Grip Strength (in kg): {grip_strength}"

            if weight == None:
                weight= 'Not filled by client.'

            if grip_strength == None:
                grip_strength_metric= '*Grip Strength (in kg)*: Not filled by client.'

            # Compose the WhatsApp message with the formatted metrics
            message = (
                f"🏋️‍♂️ *Pre-Session Report* 🏋️‍♂️\n\n"
                f"     *Dear* {coach_name},\n\n"
                f"👤 *Client*: *{client_name}*\n"
                f"🗓️ *Date*: {date.strftime('%Y-%m-%d')}\n"
                f"⚖️ *Weight (in kg)*: {weight}\n\n" 
                f"📊 *Metrics*:\n\n"
                f"{sleep_metric}\n"          
                f"{soreness_metric}\n"
                f"{mental_stress_metric}\n"  
                f"{fatigue_metric}\n"
                f"{pain_scale_metric}\n"     
                f"{stiffness_metric}\n"
                f"{grip_strength_metric}\n\n"
                f"📈 *Wellness Score*: {composite_score:.2f}%\n\n"
                f"🔔 *Review these metrics before the session and adjust training accordingly.*\n\n"
                f"*Invictus Performance Lab*"
            )
            
            # Get the coach's phone number
            coach_number = get_coach_number(coach_name)

            # # Schedule message to send immediately or with a slight delay
            # now = datetime.now()
            # hours, minutes = now.hour, now.minute + 2  # Schedule 2 minutes from now
            # if minutes >= 60:
            #     minutes -= 60
            #     hours += 1  # Send 1 minute from now to ensure time sync

            # # Send the WhatsApp message using pywhatkit
            # kit.sendwhatmsg(coach_number, message, hours, minutes)

            # Send the WhatsApp message in a background thread
            thread = Thread(target=send_whatsapp_message, args=(coach_number, message))
            thread.start()

            formatted_score = f"{composite_score:.2f}"

            # Render a success page with the composite score
            return render(request, 'success_pre.html', {'composite_score': formatted_score})

    else:
        form = PreForm()

    # Render the pre-session form page
    return render(request, 'pre_session.html', {'pre_form': form, 'client_names': client_names, 'coach_names': coach_names})


# Utility functions for calculating acwr
def fetch_records_by_client(sheet, client_name):
    """Fetch records for a specific client from the Google Sheet."""
    records = sheet.get_all_records()
    return [r for r in records if r['Client Name'] == client_name]

def get_last_acwr_value(client_name, column_name, sheet):
    """Retrieve the last ACWR value (RPE or HR) for a specific client."""
    client_records = fetch_records_by_client(sheet, client_name)
    if not client_records:
        return 0

    # Sort records by date and get the latest record
    latest_record = sorted(
        client_records, key=lambda x: datetime.strptime(x['Date'], '%Y-%m-%d')
    )[-1]

    # Retrieve and convert the ACWR value
    acwr_value = latest_record.get(column_name, 0)
    try:
        return float(acwr_value) if acwr_value else 0
    except ValueError:
        return 0

def calculate_ewma(new_value, previous_ewma, alpha):
    """Calculate the Exponentially Weighted Moving Average (EWMA)."""
    return (alpha * new_value) + (1 - alpha) * previous_ewma

def calculate_acwr(acute_load, chronic_load):
    """Calculate the ACWR, avoiding division by zero."""
    return acute_load / chronic_load if chronic_load != 0 else 0

def append_to_google_sheets(sheet, data):
    """Append data to the Google Sheet."""
    try:
        sheet.append_row(data)
        print("Data appended to Google Sheet successfully.")
    except Exception as e:
        print(f"Error appending data to Google Sheet: {e}")
        raise e  # Let the caller handle this exception

def send_whatsapp_message(coach_number, message):
    """Function to send a WhatsApp message."""
    now = datetime.now()
    hours, minutes = now.hour, now.minute + 1  # Schedule 2 minutes from now
    if minutes >= 60:
        minutes -= 60
        hours += 1  # Adjust the hour if minutes exceed 60
    kit.sendwhatmsg(coach_number, message, hours, minutes)

def post_session_view(request):
    client_names = get_client_names()
    coach_names = get_coach_names()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            client_name = form.cleaned_data['client_name']
            coach_name = form.cleaned_data['coach_name']
            date = form.cleaned_data['date']
            rpe = form.cleaned_data['rpe']
            pain_scale = form.cleaned_data['pain_scale']
            session_duration = form.cleaned_data['session_duration']
            avg_HR = form.cleaned_data.get('avg_HR')  # Using get() to handle None

            # Session load calculations
            session_load_rpe = rpe * session_duration

            # Only calculate session_load_hr if avg_HR is provided
            if avg_HR is not None:
                session_load_hr = avg_HR * session_duration
            else:
                session_load_hr = None  # Or set it to 0 or another default value if needed

            # Retrieve last ACWR values
            last_acwr_rpe = get_last_acwr_value(client_name, 'ACWR RPE', sheet1)
            last_acwr_hr = get_last_acwr_value(client_name, 'ACWR HR', sheet1)

            # Define alpha values for EWMA
            alpha_acute = 2 / (3 + 1)
            alpha_chronic = 2 / (12 + 1)

            # Calculate loads and ACWR for RPE
            acute_load_rpe = calculate_ewma(session_load_rpe, last_acwr_rpe, alpha_acute)
            chronic_load_rpe = calculate_ewma(session_load_rpe, last_acwr_rpe, alpha_chronic)
            acwr_rpe = round(calculate_acwr(acute_load_rpe, chronic_load_rpe), 2)

            # Calculate loads and ACWR for HR (only if session_load_hr is not None)
            if session_load_hr is not None:
                acute_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_acute)
                chronic_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_chronic)
                acwr_hr = round(calculate_acwr(acute_load_hr, chronic_load_hr), 2)
            else:
                acwr_hr = 0  

            # Create and save the model instance
            post_session_metrics = form.save(commit=False)
            post_session_metrics.acwr_rpe = acwr_rpe
            post_session_metrics.acwr_hr = acwr_hr
            post_session_metrics.save()  # Save to the database

            # Prepare data for Google Sheets
            data = [
                client_name,
                coach_name,
                date.strftime('%Y-%m-%d'),
                rpe,
                pain_scale,
                session_duration,
                avg_HR if avg_HR is not None else 'N/A',  # Handle None case for avg_HR
                acwr_rpe,
                acwr_hr if acwr_hr is not None else 'N/A',  # Handle None case for acwr_hr
            ]
            sheet1.append_row(data)

            # Prepare the WhatsApp message
            pain_scale_message = f"*Pain Scale*: {pain_scale}" if pain_scale is not None else "*Pain Scale*: No Pain"
            avg_HR_message = f"*Average HR*: {avg_HR}" if avg_HR is not None else "*Average HR*: Not filled by client."
            acwr_hr_message = (
                "*ACWR (HR)*: Avg_HR is not filled by client."
                if avg_HR is None
                else f"*ACWR (HR)*: {acwr_hr:.2f}"
            )
            message = (
                f"🏋️‍♂️ *Post-Session Report* 🏋️‍♂️\n\n"
                f"     *Dear* {coach_name},\n\n"
                f"👤 *Client*: *{client_name}*\n"
                f"🗓️ *Date*: {date.strftime('%Y-%m-%d')}\n"
                f"⚖️ *RPE*: {rpe}\n"
                f"⚖️ *Session Duration*: {session_duration} minutes\n"
                f"⚖️ {pain_scale_message}\n"
                f"⚖️ {avg_HR_message}\n"
                f"⚖️ *ACWR (RPE)*: {acwr_rpe:.2f}\n"
                f"❤️ {acwr_hr_message}\n\n"
                f"📈 *NOTE*: Due to insufficient data, the ACWR value might be inaccurate.\n\n"
                f"🔔 *Keep tracking metrics to ensure steady progress.*\n\n"
                f"🧬 *Invictus Performance Lab*"
            )
            coach_number = get_coach_number(coach_name)

            # Send the WhatsApp message in a background thread
            thread = Thread(target=send_whatsapp_message, args=(coach_number, message))
            thread.start()

            return redirect('success_post')

    else:
        form = PostForm()
    return render(
        request,
        'post_session.html',
        {'post_form': form, 'client_names': client_names, 'coach_names': coach_names}
    )
# Views
# def post_session_view(request):
#     print("Entering post_session_metrics view.")
#     """Handle the post-session view."""
#     client_names = get_client_names()
#     coach_names = get_coach_names()

#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             client_name = form.cleaned_data['client_name']
#             coach_name = form.cleaned_data['coach_name']
#             date = form.cleaned_data['date']
#             rpe = form.cleaned_data['rpe']
#             pain_scale = form.cleaned_data['pain_scale']
#             session_duration = form.cleaned_data['session_duration']
#             avg_HR = form.cleaned_data.get('avg_HR')  # Using get() to handle None

#             # Session load calculations
#             session_load_rpe = rpe * session_duration

#             # Only calculate session_load_hr if avg_HR is provided
#             if avg_HR is not None:
#                 session_load_hr = avg_HR * session_duration
#             else:
#                 session_load_hr = None  # Or set it to 0 or another default value if needed

#             # Retrieve last ACWR values
#             last_acwr_rpe = get_last_acwr_value(client_name, 'ACWR RPE', sheet1)
#             last_acwr_hr = get_last_acwr_value(client_name, 'ACWR HR', sheet1)

#             # Define alpha values for EWMA
#             alpha_acute = 2 / (3 + 1)
#             alpha_chronic = 2 / (12 + 1)

#             # Calculate loads and ACWR for RPE
#             acute_load_rpe = calculate_ewma(session_load_rpe, last_acwr_rpe, alpha_acute)
#             chronic_load_rpe = calculate_ewma(session_load_rpe, last_acwr_rpe, alpha_chronic)
#             acwr_rpe = round(calculate_acwr(acute_load_rpe, chronic_load_rpe), 2)

#             # Calculate loads and ACWR for HR (only if session_load_hr is not None)
#             if session_load_hr is not None:
#                 acute_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_acute)
#                 chronic_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_chronic)
#                 acwr_hr = round(calculate_acwr(acute_load_hr, chronic_load_hr), 2)
#             else:
#                 acwr_hr = 0  

#             # Create and save the model instance
#             post_session_metrics = form.save(commit=False)
#             post_session_metrics.acwr_rpe = acwr_rpe
#             post_session_metrics.acwr_hr = acwr_hr
#             post_session_metrics.save()  # Save to the database

#             # Prepare data for Google Sheets
#             data = [
#                 client_name,
#                 coach_name,
#                 date.strftime('%Y-%m-%d'),
#                 rpe,
#                 pain_scale,
#                 session_duration,
#                 avg_HR if avg_HR is not None else 'N/A',  # Handle None case for avg_HR
#                 acwr_rpe,
#                 acwr_hr if acwr_hr is not None else 'N/A',  # Handle None case for acwr_hr
#             ]
#             sheet1.append_row(data)

#             # Handle None cases for pain_scale and avg_HR in the message
#             pain_scale_message = f"*Pain Scale*: {pain_scale}" if pain_scale is not None else "*Pain Scale*: No Pain"
#             avg_HR_message = f"*Average HR*: {avg_HR}" if avg_HR is not None else "*Average HR*: Not filled by client."
#             # Handle ACWR (HR) with explicit message when avg_HR is None
#             if avg_HR is None:
#                 acwr_hr_message = "*ACWR (HR)*: Avg_HR is not filled by client."
#             else:
#                 acwr_hr_message = f"*ACWR (HR)*: {acwr_hr:.2f}"


#             # Compose the WhatsApp message with the additional metrics
#             message = (
#                 f"🏋️‍♂️ *Post-Session Report* 🏋️‍♂️\n\n"
#                 f"     *Dear* {coach_name},\n\n"
#                 f"👤 *Client*: *{client_name}*\n"
#                 f"🗓️ *Date*: {date.strftime('%Y-%m-%d')}\n"
#                 f"⚖️ *RPE*: {rpe}\n"
#                 f"⚖️ *Session Duration*: {session_duration} minutes\n"
#                 f"⚖️ {pain_scale_message}\n"
#                 f"⚖️ {avg_HR_message}\n"
#                 f"⚖️ *ACWR (RPE)*: {acwr_rpe:.2f}\n"
#                 f"❤️ {acwr_hr_message}\n\n"
#                 f"📈 *NOTE*: As we don't have enough data the ACWR value might be inaccurate.\n\n"
#                 f"🔔 *Keep tracking metrics to ensure steady progress.*\n\n"
#                 f"🧬 *Invictus Performance Lab*"
#             )

#             # Get the coach's phone number
#             coach_number = get_coach_number(coach_name)

#             # Schedule message to send immediately or with a slight delay
#             now = datetime.now()
#             hours, minutes = now.hour, now.minute + 2  # Schedule 2 minutes from now
#             if minutes >= 60:
#                 minutes -= 60
#                 hours += 1  # Send 1 minute from now to ensure time sync

#             # Send the WhatsApp message using pywhatkit
#             kit.sendwhatmsg(coach_number, message, hours, minutes)

#             return redirect('success_post')

#     # If the request method is GET, render the empty form
#     else:
#         form = PostForm()
#     return render(
#         request,
#         'post_session.html',
#         {'post_form': form, 'client_names': client_names, 'coach_names': coach_names}
#     )


# Set-ExecutionPolicy Unrestricted -Scope CurrentUser