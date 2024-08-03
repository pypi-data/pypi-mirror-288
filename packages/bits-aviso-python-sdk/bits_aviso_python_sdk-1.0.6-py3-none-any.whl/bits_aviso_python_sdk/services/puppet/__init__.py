import logging
import pypuppetdb
import requests
import ssl


class Puppet:
    """The Puppet class."""
    def __init__(self, hostname='pdb.broadinstitute.org', port=8081, ssl_cert=None, ssl_key=None, ssl_verify=None):
        """Initializes the Puppet class."""
        self.database = pypuppetdb.connect(
            host=hostname,
            port=port,
            ssl_key=ssl_key,
            ssl_cert=ssl_cert,
            ssl_verify=ssl_verify
        )
        ssl.SSLContext.hostname_checks_common_name = True

    def list_hosts(self):
        """Lists all the hosts in PuppetDB.

        Returns:
            list(str): A list of host names.
        """
        try:
            logging.info('Listing all hosts in PuppetDB...')
            hosts = [node.name for node in self.database.nodes()]
            logging.info(f'Found {len(hosts)} hosts.')
            return hosts

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list hosts: {e}")
            return

        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"Connection to PuppetDB timed out: {e}")
            return

    def list_facts(self):
        """Lists all the facts in PuppetDB for every host.

        Returns:
            list(dict): A list of dictionaries with node names as keys and their facts as values.
        """
        facts_data = []
        try:
            node_facts = {}
            logging.info('Listing all facts for all the hosts in PuppetDB...')
            for fact in self.database.facts():
                node_facts["node"] = fact.node
                node_facts[fact.name] = fact.value

                facts_data.append(node_facts)

            logging.info(f'Found {len(facts_data)} facts.')
            return facts_data

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list all the facts: {e}")
            return

        except requests.exceptions.ConnectTimeout as e:
            logging.error(f"Connection to PuppetDB timed out: {e}")
            return
