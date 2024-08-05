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
    # filters out empty matches ('') and flattens result to normal list
    return [match for sublist in matches for match in sublist if match]

class Trace:
    def __init__(self, span_id, trace_id, db_statements, http_target, start_time):
        self.span_id = span_id
        self.trace_id = trace_id
        self.db_statements = db_statements
        self.http_target = http_target
        self.start_time = start_time
        self.parent_endpoint = None

    def __repr__(self):
        return f"trace(span_id={self.span_id}, trace_id={self.trace_id}, db_statements={self.db_statements}, http_target={self.http_target}, start_time={self.start_time})"

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

def set_parent_endpoints(traces, service_name):
    # Create a dictionary to store parents
    parents = {}
    grouped = group_traces_by_trace_id(traces)

    for k, g in grouped.items():
        # sort traces of all traceids by start time
        g.sort(key=lambda x: x.start_time, reverse=False)

        # go through all traces of a traceid and find the first which is from the service
        for l in g:
            name = l.get_endpoint_name()
            if name != None and name.startswith(service_name): 
                parents[k] = name
                break

    # set parents for all traces
    for trace in traces:
        endpoint_name = trace.get_endpoint_name()
        if endpoint_name != None:
            parent = parents.get(trace.trace_id)
            if parent:
                trace.parent_endpoint = parent

    return traces

def group_traces(traces, remove_duplicates = True):
    grouped_traces = {}

    for trace in traces: 
        table_names = trace.get_table_names()

        if table_names != None and trace.parent_endpoint != None:
            endpoint_name = trace.parent_endpoint

            if endpoint_name not in grouped_traces:
                grouped_traces[endpoint_name] = []

            for name in table_names:
                if remove_duplicates:
                    if name in grouped_traces[endpoint_name]:
                        continue
                    else:
                        grouped_traces[endpoint_name].append(name)
                else: grouped_traces[endpoint_name].append(name)

    return grouped_traces


def extract_traces(result, service_name, api_type = "grpc"):
    traces = []

    value = "vStr" if api_type == "grpc" else "value" 
    span_id_value = "spanId" if api_type == "grpc" else "spanID"
    trace_id_value = "traceId" if api_type == "grpc" else "traceID"
 
    for data in result["data"]:
        for trace in data["spans"]:
            db_statements = []
            http_target = ""
            start_time = trace["startTime"]

            for tag in trace["tags"]:
                if "key" in tag:
                    if tag["key"] == "http.target":
                        http_target = tag[value]

                    if tag["key"] == "db.statement":
                        db_statements.append(tag[value])
                
            span_obj = Trace(
                span_id=trace[span_id_value], 
                trace_id=trace[trace_id_value],
                http_target = http_target,
                db_statements = db_statements,
                start_time = start_time
            )

            traces.append(span_obj)

    traces = set_parent_endpoints(traces, service_name)

    return traces


def get_number_of_calls_per_table(traces):
    grouped_traces = group_traces(traces, False)
    calls = {}

    for url, tables in grouped_traces.items():
        counter = Counter(tables)
        calls[url] = dict(counter)

    return calls

def get_number_of_endpoint_calls(traces):
    n_calls = {}

    for trace in traces:
        parent = trace.parent_endpoint
        if parent is not None or '':
            n_calls[parent] = n_calls.setdefault(parent, 0) + 1

    return n_calls

def get_grouped_traces_from_file(jsonfile, service_name, api_type = "grpc"):
    traces = extract_traces(jsonfile, service_name, api_type)

    return group_traces(traces)

def get_number_of_calls_per_table_from_file(jsonfile, service_name, api_type = "grpc"):
    traces = extract_traces(jsonfile, service_name, api_type)

    return get_number_of_calls_per_table(traces)


def get_number_of_endpoint_calls_from_file(jsonfile, service_name, api_type = "grpc"):
    traces = extract_traces(jsonfile, service_name, api_type)

    return get_number_of_endpoint_calls(traces)


def main(): 
    #file = open("../../teastore/test_data/auth_020624.json", 'r')
    file = open("../../grpc/auth.json", "r")
    #file = open("../../test_scenarios/test_data/scenario1.json", "r")
    #file = open("traces-1719816901052.json", "r")
    data = json.load(file)
    file.close()
    name = "tools.descartes.teastore.auth"
    c = extract_traces(data, name)

    grouped = group_traces(c) 
    print(grouped)


if __name__ == '__main__':
    main()

