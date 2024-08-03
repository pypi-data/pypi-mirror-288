from bits_aviso_python_sdk.helpers import export_to_json, normalize_data_for_bigquery, initialize_logger
from bits_aviso_python_sdk.services.puppet import Puppet
from bits_aviso_python_sdk.services.google.storage import Storage


def test():
    """Tests the Puppet class."""
    initialize_logger()
    st = Storage()
    bucket_name = ''
    key_path = '/tmp/key.pem'
    cert_path = '/tmp/crt.pem'
    ca_path = '/tmp/ca.pem'
    st.download_blob_to_file(bucket_name, '', key_path)
    st.download_blob_to_file(bucket_name, '', cert_path)
    st.download_blob_to_file(bucket_name, '', ca_path)
    p = Puppet(ssl_cert=cert_path, ssl_key=key_path, ssl_verify=ca_path)
    facts = p.list_facts()
    export_to_json(facts, 'facts.json')
    clean_data = normalize_data_for_bigquery(facts)
    export_to_json(clean_data, 'clean_facts.json')


if __name__ == '__main__':
    test()
