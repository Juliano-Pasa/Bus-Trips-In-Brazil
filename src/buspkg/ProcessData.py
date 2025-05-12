from datetime import date, time, datetime

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
    for i in range(len(value - 1, -1, -1)):
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


def ProcessRawTripData(entry, headerMap):
    '''
        Processes an entry of raw data from the regular trips dataset. 
        Converts all data read from this dataset's csv to their respective type to be stored in the database.

        `headerMap`: Dictionary that maps column name to its position in the entry list
    '''

    entry[headerMap['codigo_viagem']] = "".join(n for n in entry[headerMap['codigo_viagem']] if n.isnumeric())
    entry[headerMap['cnpj']] = "".join(n for n in entry[headerMap['cnpj']] if n.isnumeric())
    entry[headerMap['placa']] = "".join(n for n in entry[headerMap['placa']] if n.isalnum())
    entry[headerMap['nu_linha']] = "".join(n for n in entry[headerMap['nu_linha']] if n.isalnum())

    entry[headerMap['data_viagem_programada']] = ProcessDateTime(entry[headerMap['data_viagem_programada']], "date")
    entry[headerMap['hora_viagem_programada']] = ProcessDateTime(entry[headerMap['hora_viagem_programada']], "time")
    entry[headerMap['data_inicio_viagem']] = ProcessDateTime(entry[headerMap['data_inicio_viagem']], "datetime")
    entry[headerMap['data_fim_viagem']] = ProcessDateTime(entry[headerMap['data_fim_viagem']], "datetime")   

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
