import gspread
from config import Config
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range


def g_append(href, name):
    gc = gspread.service_account('service_account.json')
    sht2 = gc.open_by_url(Config.GOOGLE_SHEETS_URL)
    worksheet = sht2.get_worksheet(0)

    result = worksheet.append_row([name, href])
    num_row = result['updates']['updatedRange'].split(':')[0].split('!A')[1]
    print(num_row)

    validation_rule = DataValidationRule(
        BooleanCondition('BOOLEAN', ['TRUE', 'FALSE']),
        showCustomUi=True
    )
    set_data_validation_for_cell_range(worksheet, f'E{num_row}:N{num_row}', validation_rule)  # inserting checkbox
    validation_rule = DataValidationRule(
        BooleanCondition('ONE_OF_LIST', ['Prepare for test', 'Waiting for test', 'In test', 'Finished', 'Pause', 'Re-test']),
        showCustomUi=True
    )
    set_data_validation_for_cell_range(worksheet, f'C{num_row}', validation_rule)  # inserting select
    worksheet.update(f'C{num_row}', 'Prepare for test')