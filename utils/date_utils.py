from nepali_datetime import date as nep_date
import datetime

def get_nepali_month_range_ad(nepali_month_str):
    # e.g., "श्रावण २०८२"
    month_map = {
        "बैशाख": 1, "जेठ": 2, "असार": 3, "श्रावण": 4, "भदौ": 5,
        "आश्विन": 6, "कार्तिक": 7, "मंसिर": 8, "पौष": 9, "माघ": 10,
        "फाल्गुन": 11, "चैत्र": 12
    }
    parts = nepali_month_str.split()
    nepali_month = parts[0]
    nepali_year = int(parts[1])
    month_num = month_map[nepali_month]

    start_nepali_date = nep_date(nepali_year, month_num, 1)
    start_ad = start_nepali_date.to_datetime_date()

    # Handle month/year wrapping
    if month_num < 12:
        end_nepali_date = nep_date(nepali_year, month_num + 1, 1) - datetime.timedelta(days=1)
    else:
        end_nepali_date = nep_date(nepali_year + 1, 1, 1) - datetime.timedelta(days=1)

    end_ad = end_nepali_date.to_datetime_date()

    return (str(start_ad), str(end_ad))