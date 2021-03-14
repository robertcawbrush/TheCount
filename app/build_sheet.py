from re import I


def build_house(service, users, spreadsheet_id, house_range):
    body = {'values': users}
    result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=house_range,
            valueInputOption='RAW', body=body).execute()

    updated_cells = result.get('updatedCells')
    print('{0} cells updated.'.format(updated_cells))

def build_leaderboard():
    raise NotImplementedError


def check_manifest_built():
    # TODO: add aggregate functions to excel sheet
    # =COUNT house_info[user coord]
    # =SUM House points
    # =AVERAGE house points
    raise NotImplementedError
