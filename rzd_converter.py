from sys import stderr
import xlrd
import exception as ex
import logger
import json
import os.path as op
import argparse
import os

lh = logger.log_init()


def excel_empty(cell_value):
    return None


def excel_unicode_string(cell_value):
    if len(cell_value.replace(" ", "")) == 0:
        return None
    try:
        cell_value = json.loads(cell_value)
        return cell_value
    except json.JSONDecodeError:
        return cell_value


def excel_number(cell_value):
    if cell_value - int(cell_value) > 0:
        return cell_value
    return round(cell_value, 2)


def excel_date(cell_value):
    return xlrd.xldate_as_datetime(cell_value, datemode).isoformat() + "Z"


def excel_bool(cell_value):
    return cell_value == 1


def datatype_switcher(type_code, cell_value):
    try:
        convert_func = excel_data_type[type_code]
    except KeyError:
        lh.warning("Excel type convert error")
        return None
    return convert_func(cell_value)


excel_data_type = {0: excel_empty,
                   1: excel_unicode_string,
                   2: excel_number,
                   3: excel_date,
                   4: excel_bool}


def sheet_parser(sh, dt):
    dt[sh.name] = []
    keys = sh.row_values(0)
    for row in range(1, sh.nrows):
        rowsdata = {}
        for coll in range(sh.ncols):
            cell = sh.cell(row, coll)
            rowsdata[keys[coll]] = datatype_switcher(cell.ctype, cell.value)
        dt[sh.name].append(rowsdata)


def main(input_file, output_file=None):
    try:
        input_file = op.normpath(input_file)
    except IndexError:
        raise ex.ConvertErr("No input file specified")

    if output_file:
        output_file = op.normpath(output_file)
        if op.isdir(output_file):
            output_file = op.join(output_file, op.splitext(op.split(input_file)[1])[0] + ".json")
        if not op.split(output_file)[0]:
            output_file = op.join(op.split(input_file)[0], output_file)
        if op.splitext(output_file)[1] != ".json":
            raise ex.ConvertErr("define the output file in json format")
        if op.isfile(output_file):
            raise ex.ConvertErr("output file exist")
    else:
        lh.warning("No output file specified")
        output_file = op.join(op.splitext(input_file)[0] + ".json")
        if op.isfile(output_file):
            raise ex.ConvertErr("output file exist")

    try:
        rb = xlrd.open_workbook(input_file)
    except FileNotFoundError:
        raise ex.ConvertErr(f"No such file: {input_file}")
    except xlrd.biffh.XLRDError as err:
        raise ex.ConvertErr(f"Can't open file: {err}")

    data = {}
    global datemode
    datemode = rb.datemode

    for sheet in rb.sheets():
        sheet_parser(sheet, data)

    try:
        json_data = json.dumps(data, ensure_ascii=False)
    except json.JSONDecodeError as err:
        raise ex.ConvertErr(f"Can't encode data : {err}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding='utf-8') as f:
        f.write(json_data)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input")
    p.add_argument("-o", "--output")
    args = p.parse_args()

    if not args.input:
        p.print_help(stderr)
        exit()
    try:
        lh.info("start converting")
        main(args.input, args.output)
    except ex.ConvertErr as err:
        lh.error(err)
        exit()

    lh.info("done")
