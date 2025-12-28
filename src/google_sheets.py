import gspread, logging, os
from google.oauth2.service_account import Credentials

def upload_to_sheet(df):
    if df.empty:
        logging.warning("No data to upload to Google Sheets.")
        return
    try:
        creds = Credentials.from_service_account_file(
            filename=os.getenv("GOOGLE_SA_PATH"),
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(creds)
        sheet = gc.open(os.getenv("GOOGLE_SHEET_NAME")).sheet1
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        logging.info("✅ Google Sheets updated successfully.")
    except Exception as e:
        logging.error(f"Google Sheets upload failed: {e}")
