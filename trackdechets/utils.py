

def spreadsheet2array(spreadsheet, offset=0):
    """ Convert an Excel table to a Python array """
    headers = spreadsheet.row_values(offset)
    rows = []
    for r in range(offset + 1, spreadsheet.nrows):
        row = spreadsheet.row_values(r)
        rows.append(dict(zip(headers, row)))
    return rows
