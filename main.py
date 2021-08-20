import pandas as pd
import argparse as ap
import os
import re
import json
import numpy as np



def getNumbersFromString(line):
    res = re.findall(r"[-+]?\d*\.\d+|\d+", line)
    for i in range(len(res)):
        res[i] = float(res[i])
    return res

def convertOLTPToJSON(filepath):
    res = {}
    file = open(filepath, 'r')
    lines = file.readlines()

    for idx in range(len(lines)):
        line = lines[idx]
        if re.match("SQL statistics*", line):
            res["SQL statistics"] = {
                "queries performed" : {
                    "read": getNumbersFromString(lines[idx+2])[0],
                    "write": getNumbersFromString(lines[idx+3])[0],
                    "other": getNumbersFromString(lines[idx+4])[0],
                    "total": getNumbersFromString(lines[idx+5])[0]
                },
                "transactions": getNumbersFromString(lines[idx+6])[0],
                "queries": getNumbersFromString(lines[idx+7])[0],
                "ignored errors": getNumbersFromString(lines[idx+8])[0],
                "reconnects": getNumbersFromString(lines[idx+9])[0]
            }
        elif re.match("Throughput*", line):
            res["Throughput"] = {
                "events/s (eps)": getNumbersFromString(lines[idx+1])[0],
                "time elapsed (s)": getNumbersFromString(lines[idx+2])[0],
                "total number of events": getNumbersFromString(lines[idx+3])[0]
            }
        elif re.match("Latency*", line):
            res["Latency"] = {
                "min(ms)": getNumbersFromString(lines[idx+1])[0],
                "avg(ms)": getNumbersFromString(lines[idx+2])[0],
                "max(ms)": getNumbersFromString(lines[idx+3])[0],
                "95th percentile": getNumbersFromString(lines[idx+4])[1],
                "sum(ms)": getNumbersFromString(lines[idx+5])[0]
            }
        elif re.match("Threads fairness*", line):
            res["Threads fairness"] = {
                "events(avg/stddev)": "%f/%f" % (getNumbersFromString(lines[idx+1])[0], getNumbersFromString(lines[idx+1])[1]),
                "execution time (avg/stddev)": "%f/%f" % (getNumbersFromString(lines[idx+2])[0], getNumbersFromString(lines[idx+2])[1])
            }
            break
    return res

def convertOthersToJSON(filepath):
    return ""





def get_fields(sheet):
    return sheet.columns.values.tolist()

def create_single_parameter(name, value):

    return " --%s=%s" % (name, value)

def create_parameters(row, columns):
    res = ""
    null_fields = pd.isnull(row).to_dict()
    type = row["type"]


    for i in range(len(columns)):
        # ignore test col
        if type == "oltp" and columns[i] == "test":
            continue
        if i != 0 and i != 1 and null_fields[columns[i]] == False and columns[i] != "test_type":
            res += create_single_parameter(columns[i], row[columns[i]])
    return res

def get_test_name(row, general_config, mysql_config):
    t = row["type"]
    if t == "oltp":
        t = row["test_type"]
    return "general%s-mysql%s-%s%s" % (general_config, mysql_config, t, row["id"])

def get_testfile_name(row, cmd, general_config, mysql_config):
    return "%s-%s.txt" % (get_test_name(row, general_config, mysql_config), cmd)

def create_command(general_config ,mysql_config, type, row, columns, command, general_id , mysql_id):
    if command == "run":
        return "sysbench%s%s%s %s %s > %s" % (general_config, mysql_config, create_parameters(row, columns), type, command, get_testfile_name(row, command, general_id, mysql_id))
    else:
        return "sysbench%s%s%s %s %s" % (general_config, mysql_config, create_parameters(row, columns), type, command)

def get_configuration(sheet, id):
    for idx, row in sheet.iterrows():
        if int(id) == idx:
            return create_parameters(row, get_fields(sheet))


def execute_test(test_list, row, type, columns, mysql_configure_id, general_configure_id):
    print("Executing %s test.." % get_test_name(row, general_configure_id,mysql_configure_id))
    test_list.append(get_test_name(row, general_configure_id,mysql_configure_id))

    mysql_sheet = name_to_sheet["mysql"]
    mysql_config = get_configuration(mysql_sheet, mysql_configure_id)

    general_sheet = name_to_sheet["general"]
    general_config = get_configuration(general_sheet, general_configure_id)

    if re.match("oltp*", type):
        type = row["test"]

    prepare_cmd = create_command(general_config, mysql_config, type,row, columns, "prepare", general_configure_id, mysql_configure_id)
    run_cmd = create_command(general_config, mysql_config, type, row, columns, "run", general_configure_id, mysql_configure_id)
    cleanup_cmd = create_command(general_config, mysql_config, type, row, columns, "cleanup", general_configure_id, mysql_configure_id)
    prepare_filename = get_testfile_name(row, "prepare", general_configure_id, mysql_configure_id)
    run_filename = get_testfile_name(row, "run", general_configure_id, mysql_configure_id)
    cleanup_filename = get_testfile_name(row, "cleanup", general_configure_id, mysql_configure_id)


    print(prepare_cmd)

    print(run_cmd)

    print(cleanup_cmd)

    os.system(prepare_cmd)

    os.system(run_cmd)

    if row["type"] == "oltp":
        json_res = convertOLTPToJSON(run_filename)
        with open('%s.json' % get_test_name(row, general_configure_id, mysql_configure_id), 'w') as fp:
            json.dump(json_res, fp)
    else:
        json_res = convertOthersToJSON(run_filename)
        with open('%s.json' % get_test_name(row, general_configure_id, mysql_configure_id), 'w') as fp:
            json.dump(json_res, fp)


    # os.remove(run_filename)

    os.system(cleanup_cmd)

    print("Finished!\n")





file_name = "parameters.xlsx"
sheet_names = ["fileio", "cpu", "threads", "mutex", "memory","mysql", "general", "oltp"]
name_to_sheet = {}

for sheet_name in sheet_names:
    s = pd.read_excel(file_name, sheet_name, engine="openpyxl")
    name_to_sheet[sheet_name] = s


parser = ap.ArgumentParser()
parser.add_argument("config", help="specify the mysql configuration id as the context")
parser.add_argument("general", help="specify the general configuration id as the context")
parser.add_argument("type", help="specify the test type you want to execute")
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", "--all", help="execute all tests, including 'fileio', 'cpu', 'threads', 'mutex' and 'memory'", action="store_true")
group.add_argument("-c", "--case", help="specify the testcase id under certain test type that you want to execute", type=int)


args = parser.parse_args()

if args.type in sheet_names:
    sheet = name_to_sheet[args.type]
    columns = get_fields(sheet)

    config_id = int(args.config) - 1
    general_id = int(args.config) - 1

    test_list = []

    if args.all:
        for idx, row in sheet.iterrows():
            execute_test(test_list, row, args.type,columns, config_id, general_id)
    else:
        for idx, row in sheet.iterrows():
            if idx+1 == args.case:
                execute_test(test_list, row, args.type,columns, config_id, general_id)
    file = open('test_list.txt', 'w')
    file.write(str(test_list))
    file.close()

else:
    print("ERROR: type %s not found" % args.type)
