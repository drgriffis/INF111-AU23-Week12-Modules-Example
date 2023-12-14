import csv
from fema_data_model import DataRow

def loadCSVRow(csv_row, key='zipcode'):
  data = {}
  for (col_name, row_value) in csv_row.items():
    if col_name != key and col_name[:4] != 'avg_':
      data[col_name] = float(row_value)

  # pad with 0s to ensure all ZIPs are 5-digit
  key = csv_row[key]
  while len(key) < 5:
    key = '0{0}'.format(key)

  data = DataRow(
      key,
      data
  )
  return data

def loadCSV(csv_file, key='zipcode'):
  data = {}
  with open(csv_file, 'r') as stream:
    reader = csv.DictReader(stream)
    for row in reader:
      row = loadCSVRow(row, key=key)
      data[row.row_id] = row
  return data

def addRows(row_1, row_2, new_key):
  # assume both rows have the same keys
  new_data = {}
  for key in row_1.keys():
    new_data[key] = row_1.data[key] + row_2.data[key]
  return DataRow(
    new_key,
    new_data
  )

def combineAtZipLevel(data, zip_level):
  combined = {}
  for row in data.values():
    new_key = row.row_id[:zip_level]
    if not new_key in combined:
      combined[new_key] = DataRow(
          new_key,
          row.data
      )
    else:
      combined[new_key] = addRows(
          combined[new_key], # values so far
          row,               # new values to add
          new_key
      )

  # and update all percentages
  for row in combined.values():
    row.recalculatePercentages()

  return combined