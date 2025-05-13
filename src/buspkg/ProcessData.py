import csv
import pickle

from os import path

import charset_normalizer

from datetime import date, time, datetime


def DiscoverFileEncoding(filePath):
    '''
        Discover file encoding using charset_normalizer library.
    '''

    with open(filePath, 'rb') as rawdata:
        encoding = charset_normalizer.detect(rawdata.read(10000))
    return encoding


def ProcessFloatNotation(value):
    '''
        Casts a string with different number notations to a float.

        "1.000.001,23" -> "1000001.23"\n
        "1,000,001.23" -> "1000001.23"\n
        "-1000001.23"  -> "1000001.23"
    '''

    try:
        cleanValue = float(value)
        return cleanValue
    except Exception:
        pass

    decimalPointIdx = -1
    for i in range(len(value) - 1, -1, -1):
        if value[i] == '.' or value[i] == ',':
            decimalPointIdx = i
            break

    result = ""
    for i in range(len(value)):
        if i == decimalPointIdx:
            result += "."
        elif value[i].isnumeric() or value[i] == '-':
            result += value[i]

    return float(result)


def ProcessDateTime(entry, mode):
    '''
        Casts a datetime string to datetime type.

        `mode`: Specifies if entry is 'date', 'time' or 'datetime'
    '''

    if not len(entry):
        return None
    
    if mode == "date":
        d, m, Y = map(int, entry.split("-"))
        return date(day=d, month=m, year=Y)
    if mode == "time":
        return time.fromisoformat(entry)
    if mode == "datetime":
        dateSplit, timeSplit = entry.split(" ")
        d, m, Y = map(int, dateSplit.split("-"))

        dateParsed = date(day=d, month=m, year=Y)
        timeParsed = time.fromisoformat(timeSplit)

        return datetime.combine(dateParsed, timeParsed)
    
    raise Exception(f"Invalid mode was given in ProcessDateTime: {mode}")


def ProcessRawTripEntry(entry, headerMap):
    '''
        Processes an entry of raw data from the regular trips dataset. 
        Converts all data read from this dataset's csv to their respective type to be stored in the database.
        It also filters out any entry that does not fall into the database partition range from 01-01-2019 to 31-12-2024.

        `headerMap`: Dictionary that maps column name to its position in the entry list
    '''

    entry[headerMap['data_inicio_viagem']] = ProcessDateTime(entry[headerMap['data_inicio_viagem']], "datetime")

    firstDatetime = datetime(year=2019, month=1, day=1)
    lastDatetime = datetime(year=2024, month=12, day=31)
    tripStart = entry[headerMap['data_inicio_viagem']]

    if tripStart < firstDatetime or tripStart > lastDatetime:
        return None

    entry[headerMap['data_viagem_programada']] = ProcessDateTime(entry[headerMap['data_viagem_programada']], "date")
    entry[headerMap['hora_viagem_programada']] = ProcessDateTime(entry[headerMap['hora_viagem_programada']], "time")
    entry[headerMap['data_fim_viagem']] = ProcessDateTime(entry[headerMap['data_fim_viagem']], "datetime")

    entry[headerMap['codigo_viagem']] = "".join(n for n in entry[headerMap['codigo_viagem']] if n.isnumeric())
    entry[headerMap['cnpj']] = "".join(n for n in entry[headerMap['cnpj']] if n.isnumeric())
    entry[headerMap['placa']] = "".join(n for n in entry[headerMap['placa']] if n.isalnum())
    entry[headerMap['nu_linha']] = "".join(n for n in entry[headerMap['nu_linha']] if n.isalnum())

    # entry[headerMap['tipo_viagem']] is just a string, no processing needed.

    lineDirection = entry[headerMap['sentido_linha']]
    if lineDirection != '0' and lineDirection != '1':
        raise Exception(f"Invalid value for 'sentido_linha': {entry[headerMap['sentido_linha']]}. Values should be either 0 or 1.")

    entry[headerMap['latitude']] = ProcessFloatNotation(entry[headerMap['latitude']])
    entry[headerMap['longitude']] = ProcessFloatNotation(entry[headerMap['longitude']])
    entry[headerMap['pdop']] = ProcessFloatNotation(entry[headerMap['pdop']])

    transbordoValue = entry[headerMap['in_transbordo']].lower()
    if transbordoValue == 'não':
        entry[headerMap['in_transbordo']] = False
    elif transbordoValue == 'sim':
        entry[headerMap['in_transbordo']] = True
    else:
        raise Exception(f"Invalid value for 'in_transbordo': {transbordoValue}. Values should be either 'não' or 'sim'.")

    return entry


def ProcessRawTripFile(filePath, encoding):
    '''
        Processes all rows of a raw trip data file.
    '''

    with open(filePath, encoding=encoding) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        header = next(reader)
        headerMap = dict(zip(header ,range(len(header))))

        batch = []
        for row in reader:
            processedEntry = ProcessRawTripEntry(row, headerMap)
            if not processedEntry:
                continue
            batch.append(processedEntry)
    return batch


def GetPickleCheckpoint(picklePath):
    ''' 
        Loads content from a pickle file. Returns `None` if file does not exist.
    '''

    if not path.exists(picklePath):
        return None
    with open(picklePath, 'rb') as p:
        result = pickle.load(p)
    return result


def SavePickleCheckpoint(picklePath, data):
    '''
        Saves content to pickle file. Overwrites file if it already existed.
    '''

    with open(picklePath, 'wb') as p:
        pickle.dump(data, p)