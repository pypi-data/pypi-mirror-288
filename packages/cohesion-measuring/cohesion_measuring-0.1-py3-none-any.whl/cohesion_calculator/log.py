import json
from collections import Counter
import re

def is_number(value):
   try:
        float(value)
        return True
   except ValueError:
        return False

table_name_pattern = re.compile(
    r"""
    (?i)   # Case-insensitive matching
    \bFROM\s+([`'"]?[a-zA-Z_][\w$]*[`'"]?)|   
    \bJOIN\s+([`'"]?[a-zA-Z_][\w$]*[`'"]?)|   
    \bINTO\s+([`'"]?[a-zA-Z_][\w$]*[`'"]?)|  
    \bUPDATE\s+([`'"]?[a-zA-Z_][\w$]*[`'"]?)| 
    \bDELETE\s+FROM\s+([`'"]?[a-zA-Z_][\w$]*[`'"]?)  
    """,
    re.VERBOSE
)

def extract_table_names(sql):
    matches = table_name_pattern.findall(sql)
    #matches = [
    #('employees', '', '', '', '', '', ''),
    #('', 'customers', '', '', '', '', '')]
    # filters out empty matches ('') and flattens result to normal list
    return [match for sublist in matches for match in sublist if match]

class Log:
    def __init__(self, span_id, trace_id, db_statements, http_target, start_time):
        self.span_id = span_id
        self.trace_id = trace_id
        self.db_statements = db_statements
        self.http_target = http_target
        self.start_time = start_time
        self.parent_endpoint = None

    def __repr__(self):
        return f"Log(span_id={self.span_id}, trace_id={self.trace_id}, db_statements={self.db_statements}, http_target={self.http_target}, start_time={self.start_time})"

    def get_endpoint_name(self):
        endpoint_name = self.http_target

        if endpoint_name != None:
            endpoint =  endpoint_name.split('?')[0]
            endpoint_parts = endpoint.split('/')

            # if the last part is a number (e.g. /customers/count/9), it should get cut - else (e.g. /customers) 
            if is_number(endpoint_parts[-1]):
                endpoint_name = '/'.join(endpoint_parts[:-1]) + '/'
            else: 
                endpoint_name = '/'.join(endpoint_parts) + '/'

            # removes duplicate / and ensures there is exactly one / at the end
            endpoint_name = '/'.join(part for part in endpoint_name.split('/') if part) + '/'
    
        return endpoint_name


    def get_db_statement(self):
        db_statements = self.db_statements

        if len(db_statements) > 0:
            return db_statements

        return None

    def get_table_names(self):
        statement = self.get_db_statement()

        if statement is not None:
            return extract_table_names(statement[0])

        return None

def group_traces_by_trace_id(traces):
    grouped_traces = {}

    for trace in traces:
        trace_id = trace.trace_id
        if trace_id not in grouped_traces:
            grouped_traces[trace_id] = []
        grouped_traces[trace_id].append(trace)

    return grouped_traces

def set_parent_endpoints(logs, service_name):
    # Create a dictionary to store parents
    parents = {}
    grouped = group_traces_by_trace_id(logs)

    for k, g in grouped.items():
        # sort traces of all traceids by start time
        g.sort(key=lambda x: x.start_time, reverse=False)

        # go through all logs of a traceid and find the first which is from the service
        for l in g:
            name = l.get_endpoint_name()
            if name != None and name.startswith(service_name): 
                parents[k] = name
                break

    # set parents for all logs
    for log in logs:
        endpoint_name = log.get_endpoint_name()
        if endpoint_name != None:
            parent = parents.get(log.trace_id)
            if parent:
                log.parent_endpoint = parent

    return logs

def group_logs(logs, remove_duplicates = True):
    grouped_logs = {}

    for log in logs: 
        table_names = log.get_table_names()

        if table_names != None and log.parent_endpoint != None:
            endpoint_name = log.parent_endpoint

            if endpoint_name not in grouped_logs:
                grouped_logs[endpoint_name] = []

            for name in table_names:
                if remove_duplicates:
                    if name in grouped_logs[endpoint_name]:
                        continue
                    else:
                        grouped_logs[endpoint_name].append(name)
                else: grouped_logs[endpoint_name].append(name)

    return grouped_logs


def extract_logs(result, service_name, api_type = "grpc"):
    logs = []

    value = "vStr" if api_type == "grpc" else "value" 
    span_id_value = "spanId" if api_type == "grpc" else "spanID"
    trace_id_value = "traceId" if api_type == "grpc" else "traceID"
 
    for data in result["data"]:
        for log in data["spans"]:
            db_statements = []
            http_target = ""
            start_time = log["startTime"]

            for tag in log["tags"]:
                if "key" in tag:
                    if tag["key"] == "http.target":
                        http_target = tag[value]

                    if tag["key"] == "db.statement":
                        db_statements.append(tag[value])

            """if "references" in log:   
                for reference in log["references"]:
                    if "span" in reference: 
                        for tag in reference["span"]["tags"]:
                            if tag["key"] == "db.sql.table":
                                db_tables.append(tag[value])
                            if tag["key"] == "http.target":
                                http_target = tag[value]
                            if tag["key"] == "db.statement":
                                db_statements.append(tag[value])"""
                
            span_obj = Log(
                span_id=log[span_id_value], 
                trace_id=log[trace_id_value],
                http_target = http_target,
                db_statements = db_statements,
                start_time = start_time
            )

            logs.append(span_obj)

    logs = set_parent_endpoints(logs, service_name)

    return logs


def get_number_of_calls_per_table(logs):
    grouped_logs = group_logs(logs, False)
    calls = {}

    for url, tables in grouped_logs.items():
        counter = Counter(tables)
        calls[url] = dict(counter)

    return calls

def get_number_of_endpoint_calls(logs):
    n_calls = {}

    for log in logs:
        parent = log.parent_endpoint
        if parent is not None or '':
            n_calls[parent] = n_calls.setdefault(parent, 0) + 1

    return n_calls

def get_grouped_logs_from_file(jsonfile, service_name, api_type = "grpc"):
    logs = extract_logs(jsonfile, service_name, api_type)

    return group_logs(logs)

def get_number_of_calls_from_file(jsonfile, service_name, api_type = "grpc"):
    logs = extract_logs(jsonfile, service_name, api_type)

    return get_number_of_calls_per_table(logs)


def get_number_of_endpoint_calls_from_file(jsonfile, service_name, api_type = "grpc"):
    logs = extract_logs(jsonfile, service_name, api_type)

    return get_number_of_endpoint_calls(logs)


def main(): 
    #file = open("../../teastore/test_data/auth_020624.json", 'r')
    #file = open("../../http_api/auth_jaegerui.json", "r")
    #file = open("../../http_api/auth.json", "r")
    #file = open("../../grpc/auth.json", "r")
    #file = open("../../test_scenarios/test_data/scenario1.json", "r")
    file = open("../../http_api/auth.json", "r")
    data = json.load(file)
    file.close()
    name = "tools.descartes.teastore.auth"
    c = extract_logs(data, name, "json")

    grouped = group_logs(c) 
    print(grouped)


if __name__ == '__main__':
    main()

