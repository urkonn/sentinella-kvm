import os
import logging

import trollius as asyncio
from trollius import From

import libvirt

logger = logging.getLogger(__name__)

frequency = 60
hostname = os.uname()[1].split('.')[0]


@asyncio.coroutine
def get_stats(agent):
    yield From(agent.run_event.wait())

    """
    After plugin installation, copy the configuration file
    from sentinella-plugin-template/conf/ to /etc/sentinella/conf.d/
    """
    config = agent.config['sentinella-kvm']
    
    """
    The plugin Key is a unique UUID provided by Sentinel.la.
    If not valid, the plugin metrics will never be registered.
    """

    plugin_key = config['plugin_key']

    logger.info('starting "get_stats" task for plugin_key "%s"  and host "%s"'.format(plugin_key, hostname))

    while agent.run_event.is_set():
        yield From(asyncio.sleep(frequency))
        try:
            data = {'server_name': hostname,
                    'plugins': {}}
            logger.debug('connecting to data source')
            
            data['plugins'].update({"{}".format(plugin_key):{}})
            
            conn = libvirt.open('qemu:///system')
            for id in conn.listDomains():
                domain = conn.lookupByID(id)
                domain_name = domain.name()
                dom_info = domain.info()
                metric = "{0}_domain_name".format(domain_name)
                data['plugins'][plugin_key].update({metric:{"value":domain_name, "type":"string"}})
                cpu_time = dom_info[4]
                metric = "{0}_cpu_time".format(cpu_time)
                data['plugins'][plugin_key].update({metric:{"value":cpu_time,"type":"integer"}})
                memory = dom_info[2]
                metric = "{0}_memory".format(memory)
                data['plugins'][plugin_key].update({metric:{"value":memory,"type":"integer" }})

            logger.debug('{}: myplugin={}%'.format(hostname, data))

            yield From(agent.async_push(data))

        except:

            logger.exception('cannot get data source information')

    logger.info('get_stats terminated')
