format = data.format()
type = None

if format:
    if isinstance(format, list):
        format = format[0]
    if len(format) > 10:
        type = 'big'
    else:
        type = 'small'
else:
    data.ignore()
    type = 'ignored'

########################################

data_format = data.format()
data_type = None

if data_format:
    if isinstance(data_format, list):
        data_format = data_format[0]
    if len(data_format) > 10:
        data_type = 'big'
    else:
        data_type = 'small'
else:
    data.ignore()
    data_type = 'ignored'