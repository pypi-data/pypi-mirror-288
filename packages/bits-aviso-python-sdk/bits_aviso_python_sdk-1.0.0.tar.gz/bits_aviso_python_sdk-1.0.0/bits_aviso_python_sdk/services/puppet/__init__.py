import logging
import pypuppetdb
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
            return [node.name for node in self.database.nodes()]

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list hosts: {e}")
            return

    def list_facts(self):
        """Lists all the facts in PuppetDB for every host.

        Returns:
            list(dict): A list of dictionaries with node names as keys and their facts as values.
        """
        facts_data = []
        try:
            node_facts = {}
            for fact in self.database.facts():
                node_name = fact.node
                if node_name not in node_facts:
                    node_facts[node_name] = {}
                node_facts[node_name][fact.name] = fact.value

            for node, facts in node_facts.items():
                facts_data.append({node: facts})

        except (AttributeError, KeyError, IndexError) as e:
            logging.error(f"Unable to list all the facts: {e}")
            return

        return facts_data
