import config
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


def open_sheet():
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	cred = config.GCP_CRED
	json_obj = json.loads(cred)
	credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_obj, scope)
	gc = gspread.authorize(credentials)
	wks = gc.open("pi-thon database").sheet1
