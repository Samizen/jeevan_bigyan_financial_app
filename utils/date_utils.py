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


def bs_to_ad_date(nepali_date_str):
    """Converts a Nepali date string (YYYY-MM-DD) to a standard AD date string."""
    try:
        # VVVV CORRECTED LOGIC VVVV
        # Parse the year, month, and day from the string
        year, month, day = map(int, nepali_date_str.split('-'))
        
        # Create a nepali_datetime date object
        nepali_date_obj = nep_date(year, month, day)
        
        # Convert it to a standard Python datetime.date object
        ad_date = nepali_date_obj.to_datetime_date()
        
        # Return the formatted AD date string
        return ad_date.strftime('%Y-%m-%d')
    except (ValueError, TypeError) as e:
        # This will catch errors if the string format is incorrect
        print(f"Error converting Nepali date '{nepali_date_str}': {e}")
        return None
