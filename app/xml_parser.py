# app/xml_parser.py

import xmltodict
import pandas as pd

def parse_xml_to_dataframe(xml_file: str) -> pd.DataFrame:
    with open(xml_file) as fd:
        xml_data = xmltodict.parse(fd.read())
    return pd.DataFrame(xml_data['openimmo'])
