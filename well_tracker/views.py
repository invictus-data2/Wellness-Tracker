from django.shortcuts import render, redirect
from .forms import PreForm, PostForm
from .models import PreSessionMetrics, PostSessionMetrics
from datetime import datetime
from django.templatetags.static import static
import pywhatkit as kit
import matplotlib.pyplot as plt
import os
from .utils import get_client_names, get_coach_names

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json= {
  "type": "service_account",
  "project_id": "driven-terra-422205-u3",
  "private_key_id": "0d9e401e37 85c20b354033e5f6bbaf4b8b36353e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIXGHiGxfwMCFZ\n5QG9HnEbA+SgXn7tDj9aQYNMjIfedo+8BP4JuaEPJTxm9IvQchzgVfMtceyMGjeW\nQm8N0a2Sze+z/CDBW7q6iaNhobp8Gtp4kFsN4bVUgsIUdL7Xplc58Uzpjbt/TQ5H\nYeYE60wEsz9uC/MugZvTs5mDaQDTP3bDCVfU7U/e+zX1kgffwbVSNwQglODRsHCp\nOLgr9FupN7qckEjDcvhHOIDMRzPPHWEX+y8//3M+d7Jn1xpH6Nx7IhvjhMySK3lI\n5N+g+buVFCgfYmiAbk/UO1BFJcZhTrHg/X3k8ild4GZd1hq0f2z6/5sDynHTG14t\nyFSrRApRAgMBAAECggEAAfj7T/ICV1MjwrJBDD1GJyFhdaCDNPJ9hIRL72g4kHIF\nRAaB4/30M2yG+yeeT2+cnkd2yxtpsY752jyHNAn1p9kgv8wbVR3JFBFLDtORklYc\ndL6/Fr8e6APC4Z6tEeDl7A7k5J9PmZcjZhKDcuS6Jhd5ryvJ1iBgwux6S2/pUvIy\n3r5eLzdsaM2IARmcQLTI/K36RCeZGd0OGcbB3aT2kIXdc3+9TCjjGuSbYqfuwnxC\neppRXS7jjalAfeGzCLOr9w5LaSFAeGFiIfFJPoS3JmM1mD1yFzgYQXyw33S2C8yC\ncWUp7kOGHCIHej4ZGOVogt4Ell9kCcKsuU7xpgcoPQKBgQDzwfRqoMku4+Oy1SlM\nrhnKSRA4BVp8rhXkQ2iYLc+0FzAffb6u4UpdgeeL7ShRnLSb6sU7KbJGTy9kPJGU\nYZO0UkxrHn6IqmKhN523t0gYlQg3oUJciB1Sl1zlzxM/HW8IbDssgQoId4ujal6k\n1/2crMPgIedckzNSaq+Sp2S4zwKBgQDSbHdDmSmcjHZ1hLj1LArKI/gWxwk5MZrT\nv+PtwM0QQVEEbTbEpDwHcE2KK50cC+pkus2phHUAGkxYNiD3WM4gEV3nT3PBCBGO\nfji1z5ybjZemphgRhoES1DBQkb8Nm/+/crX6Jz39U8hJK1uvN8hGm5zM7zWUMp5d\nU1drWw+S3wKBgFzAG2mLPqIJ8rU0aN+Vi5iuDm7SkqjIcOoHQEBPhi3neNcyuKDA\ndtR3vow+tE3Bi/Ob9GpbpkscjFLevSIxsss1WYCU/N6xvo/LosaqBdPcuWC5io+8\n9zNbBu0myxMD9yDEVgvMGe441rhanCKrUQQRtQKOxAM0u52LnLz31tp/AoGAD0Eb\nuEPPN3EbWVOg0O07bwIChywwp/vHnJgpnt++PfJuPCLquICrdWKXzG9y+UiH2nuM\nU0Ct9q7xX+e0phnC/6Iiq5Uf8Bt0ol7WH6AIW2J9XvBliEe27bWCNyUJs6Pee3OG\na7cSkF3VhDBneiFSHIRFbrncqXyt7FgRW1ADpgMCgYEApzjwXJ2Luph0eL2LTF4j\nqjC4GpyV9nxA8ULtxIC5HblUrzt46SHp7jex781seY9uSS+1qvcMD/rUG6CGLKQb\nwC2x/9qX6qaxV+cRdYO0RfkxYei/rcEzWcoHdXYlYpQkVuwguvyjOU6rSGcbZSCc\n1DzILAUGtiDefe61ngmCloY=\n-----END PRIVATE KEY-----\n",
  "client_email": "chatterjee-20@driven-terra-422205-u3.iam.gserviceaccount.com",
  "client_id": "105464373381649806312",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/chatterjee-20%40driven-terra-422205-u3.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
client = gspread.authorize(credentials)
sheet = client.open("Wellness").worksheet("pre_Session")
sheet1 = client.open("Wellness").worksheet("post_Session")

def index(request): 
    return render(request, 'home.html')  

def success_pre_view(request):
    return render(request, 'success_pre.html')  # Ensure this template exists

def success_post_view(request):
    return render(request, 'success_post.html')  # Ensure this template exists

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
                (w_sleep * sleep) +
                (w_sore * (5 - soreness)) +
                (w_stress * (5 - mental_stress)) +
                (w_fatigue * (5 - fatigue)) +
                (w_pain * (5 - pain_scale)) +
                (w_stiffness * (5 - stiffness))
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
            grip_strength_metric = f"Grip Strength: {grip_strength} kg"

            # Compose the WhatsApp message with the formatted metrics
            message = (
                f"🏋️‍♂️ *Pre-Session Report* 🏋️‍♂️\n\n"
                f"     *Dear* {coach_name},\n\n"
                f"👤 *Client*: *{client_name}*\n"
                f"🗓️ *Date*: {date.strftime('%Y-%m-%d')}\n"
                f"⚖️ *Weight*: {weight} kg\n\n" 
                f"📊 *Metrics*:\n\n"
                f"{sleep_metric}\n"          
                f"{soreness_metric}\n"
                f"{mental_stress_metric}\n"  
                f"{fatigue_metric}\n"
                f"{pain_scale_metric}\n"     
                f"{stiffness_metric}\n"
                f"{grip_strength_metric}\n\n"
                f"📈 *Wellness Score*: {composite_score*2:.2f}%\n\n"
                f"🔔 *Review these metrics before the session and adjust training accordingly.*\n\n"
                f"*Invictus Performance Lab*"
            )

            # Schedule message to send immediately or with a slight delay
            now = datetime.now()
            hours, minutes = now.hour, now.minute + 2  # Schedule 2 minutes from now
            if minutes >= 60:
                minutes -= 60
                hours += 1  # Send 1 minute from now to ensure time sync

            # Send the WhatsApp message using pywhatkit
            kit.sendwhatmsg('+917319419671', message, hours, minutes)

            # Render a success page with the composite score
            return render(request, 'success_pre.html', {'composite_score': composite_score})

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

# Views
def post_session_view(request):
    """Handle the post-session view."""
    client_names = get_client_names()
    coach_names = get_coach_names()
    form = PostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Extract form data
        client_name = form.cleaned_data['client_name']
        coach_name = form.cleaned_data['coach_name']
        date = form.cleaned_data['date']
        rpe = form.cleaned_data['rpe']
        pain_scale = form.cleaned_data['pain_scale']
        session_duration = form.cleaned_data['session_duration']
        avg_HR = form.cleaned_data['avg_HR']

        # Session loads
        session_load_rpe = rpe * session_duration
        session_load_hr = avg_HR * session_duration

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

        # Calculate loads and ACWR for HR
        acute_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_acute)
        chronic_load_hr = calculate_ewma(session_load_hr, last_acwr_hr, alpha_chronic)
        acwr_hr = round(calculate_acwr(acute_load_hr, chronic_load_hr), 2)

        # Save data to the database
        form.save()

        # Prepare data for Google Sheets
        data = [
            client_name,
            coach_name,
            date.strftime('%Y-%m-%d'),
            rpe,
            pain_scale,
            session_duration,
            avg_HR,
            acwr_rpe,
            acwr_hr
        ]

        try:
            append_to_google_sheets(sheet1, data)
            message = (
                f"🏋️‍♂️ *Post-Session Report* 🏋️‍♂️\n\n"
                f"     *Dear* {coach_name},\n\n"
                f"👤 *Client*: *{client_name}*\n"
                f"🗓️ *Date*: {date.strftime('%Y-%m-%d')}\n"
                f"⚖️ *ACWR (RPE)*: {acwr_rpe:.2f}\n"
                f"❤️ *ACWR (HR)*: {acwr_hr:.2f}\n\n"
                f"📈 *Training Suggestions*: Maintain a balance between acute and chronic load to optimize performance and prevent injury.\n\n"
                f"🔔 *Keep tracking metrics to ensure steady progress.*\n\n"
                f"🧬 *Invictus Performance Lab*"
            )

            
            # Schedule message to send immediately or with a slight delay
            now = datetime.now()
            hours, minutes = now.hour, now.minute + 2  # Schedule 2 minutes from now
            if minutes >= 60:
                minutes -= 60
                hours += 1  # Send 1 minute from now to ensure time sync

            # Send the WhatsApp message using pywhatkit
            kit.sendwhatmsg('+917319419671', message, hours, minutes)

        except Exception as e:
            return render(request, 'error.html', {'error': str(e)})

        return redirect('success_post')

    return render(
        request,
        'post_session.html',
        {'post_form': form, 'client_names': client_names, 'coach_names': coach_names}
    )
