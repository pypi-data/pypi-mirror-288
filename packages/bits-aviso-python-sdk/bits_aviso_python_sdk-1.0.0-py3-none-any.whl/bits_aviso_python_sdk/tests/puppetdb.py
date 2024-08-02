from bits_aviso_python_sdk.helpers import initialize_logger
from bits_aviso_python_sdk.services.puppet import Puppet
from bits_aviso_python_sdk.services.google.storage import Storage
from bits_aviso_python_sdk.helpers import export_list_of_dicts_to_file


def test():
    """Tests the Puppet class."""
    initialize_logger()
    st = Storage()
    key_path = '/tmp/datalake_broadinstitute.org.key.pem'
    cert_path = '/tmp/datalake_broadinstitute.org.crt.pem'
    ca_path = '/tmp/ca.pem'
    # ssl_key = st.download_blob_to_file('bits-aviso-puppet-db-ssl-certs-dev', 'datalake_broadinstitute.org.priv.pem',
    #                                    key_path)
    # ssl_cert = st.download_blob_to_file('bits-aviso-puppet-db-ssl-certs-dev', 'datalake_broadinstitute.org.pem',
    #                                     cert_path)
    # ssl_ca = st.download_blob_to_file('bits-aviso-puppet-db-ssl-certs-dev', 'ca.pem', ca_path)
    p = Puppet(ssl_cert=cert_path, ssl_key=key_path, ssl_verify=ca_path)
    print(p.list_hosts())


if __name__ == '__main__':
    test()
