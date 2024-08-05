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

class Span:
    def __init__(self, span_id, trace_id, db_statements, http_target, start_time):
        self.span_id = span_id
        self.trace_id = trace_id
        self.db_statements = db_statements
        self.http_target = http_target
        self.start_time = start_time
        self.parent_endpoint = None

    def __repr__(self):
        return f"span(span_id={self.span_id}, trace_id={self.trace_id}, db_statements={self.db_statements}, http_target={self.http_target}, start_time={self.start_time})"

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

def group_spans_by_trace_id(spans):
    grouped_spans = {}

    for span in spans:
        trace_id = span.trace_id
        if trace_id not in grouped_spans:
            grouped_spans[trace_id] = []
        grouped_spans[trace_id].append(span)

    return grouped_spans

def set_parent_endpoints(spans, service_name):
    # Create a dictionary to store parents
    parents = {}
    grouped = group_spans_by_trace_id(spans)

    for k, g in grouped.items():
        # sort spans of all traceids by start time
        g.sort(key=lambda x: x.start_time, reverse=False)

        # go through all spans of a traceid and find the first which is from the service
        for l in g:
            name = l.get_endpoint_name()
            if name != None and name.startswith(service_name): 
                parents[k] = name
                break

    # set parents for all spans
    for span in spans:
        endpoint_name = span.get_endpoint_name()
        if endpoint_name != None:
            parent = parents.get(span.trace_id)
            if parent:
                span.parent_endpoint = parent

    return spans

def group_spans(spans, remove_duplicates = True):
    grouped_spans = {}

    for span in spans: 
        table_names = span.get_table_names()

        if table_names != None and span.parent_endpoint != None:
            endpoint_name = span.parent_endpoint

            if endpoint_name not in grouped_spans:
                grouped_spans[endpoint_name] = []

            for name in table_names:
                if remove_duplicates:
                    if name in grouped_spans[endpoint_name]:
                        continue
                    else:
                        grouped_spans[endpoint_name].append(name)
                else: grouped_spans[endpoint_name].append(name)

    return grouped_spans


def extract_spans(result, service_name, api_type = "grpc"):
    spans = []

    value = "vStr" if api_type == "grpc" else "value" 
    span_id_value = "spanId" if api_type == "grpc" else "spanID"
    trace_id_value = "traceId" if api_type == "grpc" else "traceID"
 
    for data in result["data"]:
        for span in data["spans"]:
            db_statements = []
            http_target = ""
            start_time = span["startTime"]

            for tag in span["tags"]:
                if "key" in tag:
                    if tag["key"] == "http.target":
                        http_target = tag[value]

                    if tag["key"] == "db.statement":
                        db_statements.append(tag[value])
                
            span_obj = Span(
                span_id=span[span_id_value], 
                trace_id=span[trace_id_value],
                http_target = http_target,
                db_statements = db_statements,
                start_time = start_time
            )

            spans.append(span_obj)

    spans = set_parent_endpoints(spans, service_name)

    return spans


def get_number_of_calls_per_table(spans):
    grouped_spans = group_spans(spans, False)
    calls = {}

    for url, tables in grouped_spans.items():
        counter = Counter(tables)
        calls[url] = dict(counter)

    return calls

def get_number_of_endpoint_calls(spans):
    n_calls = {}

    for span in spans:
        parent = span.parent_endpoint
        if parent is not None or '':
            n_calls[parent] = n_calls.setdefault(parent, 0) + 1

    return n_calls

def get_grouped_spans_from_file(jsonfile, service_name, api_type = "grpc"):
    spans = extract_spans(jsonfile, service_name, api_type)

    return group_spans(spans)

def get_number_of_calls_per_table_from_file(jsonfile, service_name, api_type = "grpc"):
    spans = extract_spans(jsonfile, service_name, api_type)

    return get_number_of_calls_per_table(spans)


def get_number_of_endpoint_calls_from_file(jsonfile, service_name, api_type = "grpc"):
    spans = extract_spans(jsonfile, service_name, api_type)

    return get_number_of_endpoint_calls(spans)
