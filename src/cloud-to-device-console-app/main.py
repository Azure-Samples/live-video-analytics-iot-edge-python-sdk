import json
from os import path
import pathlib
import logging
from builtins import input
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult
from azure.media.analyticsedge import *
from crv import Cvr
from evr import Evr
from motion_detection import MotionDetection

def graph_topologies(index):
    switcher={
            '1': Cvr().build(),
            '2': Evr().build(),
            '3': MotionDetection().build()
        }
    return switcher.get(index, None)

class GraphManager:
    
    def __init__(self):
        config_data = pathlib.Path('appsettings.json').read_text()
        config = json.loads(config_data)

        self.device_id = config['deviceId']
        self.module_id = config['moduleId']
        self.api_version = '2.0'
        self.graph_instance_name = "graphInstance1"

        self.registry_manager = IoTHubRegistryManager(config['IoThubConnectionString'])
        self.rtsp_url = config['rtspUrl']

    def invoke_wait_for_input(self, message):
        print(message)
        return input()

    def invoke_module_method(self, method):
        method_name =  method.method_name
        payload = method.serialize()
        direct_method = CloudToDeviceMethod(method_name=method_name, payload=payload)
        
        print("\n-----------------------  Request: %s  --------------------------------------------------\n" % method_name)
        print(json.dumps(payload, indent=4))
        
        resp = self.registry_manager.invoke_device_module_method(self.device_id, self.module_id, direct_method)
        
        print("\n---------------  Response: %s - Status: %s  ---------------\n" % (method_name, resp.status))

        if resp.payload is not None and 'error' in resp.payload:
            raise Exception(json.dumps(resp.payload['error'], indent=4))
        else:
            print(json.dumps(resp.payload, indent=4))
    
    def graph_topology_set(self, graph_topology):
        self.invoke_module_method(MediaGraphTopologySetRequest(graph=graph_topology))

    def graph_topology_list(self):
        self.invoke_module_method(MediaGraphTopologyListRequest())

    def graph_topology_get(self, graph_topology_name):
        self.invoke_module_method(MediaGraphTopologyGetRequest(name=graph_topology_name))

    def graph_topology_delete(self, graph_topology_name):
        self.invoke_module_method(MediaGraphTopologyDeleteRequest(name=graph_topology_name))

    def graph_instance_set(self, graph_instance):
        self.invoke_module_method(MediaGraphInstanceSetRequest(instance=graph_instance))

    def graph_instance_list(self):
        self.invoke_module_method(MediaGraphInstanceListRequest())

    def graph_instance_activate(self, graph_instance_name):
        self.invoke_module_method(MediaGraphInstanceActivateRequest(name=graph_instance_name))

    def graph_instance_deactivate(self, graph_instance_name):
        self.invoke_module_method(MediaGraphInstanceDeActivateRequest(name=graph_instance_name))
    
    def graph_instance_delete(self, graph_instance_name):
        self.invoke_module_method(MediaGraphInstanceDeleteRequest(name=graph_instance_name))
    
    def create_graph_instance(self, graph_topology, rtsp_url):
        graph_instance_name = "Sample-Graph-1"
        url_param = MediaGraphParameterDefinition(name="rtspUrl", value=rtsp_url)
        graph_instance_properties = MediaGraphInstanceProperties(description="Sample graph description", topology_name=graph_topology.name, parameters=[url_param])

        graph_instance = MediaGraphInstance(name=graph_instance_name, properties=graph_instance_properties)

        return graph_instance

if __name__ == '__main__':
    manager = GraphManager()
    
    selected_graph_topology = manager.invoke_wait_for_input("Choose the graph topology to test: 1-CRV, 2-EVR or 3-Motion detection")

    graph_topology = graph_topologies(selected_graph_topology)

    if(graph_topology is None):
        print('The selection option {} is invalid.'.format(selected_graph_topology))
    else:
        graph_instance = manager.create_graph_instance(graph_topology, manager.rtsp_url)

        try:
            manager.graph_topology_list()
            manager.invoke_wait_for_input("Press Enter to continue")

            manager.graph_topology_set(graph_topology)
            manager.invoke_wait_for_input("Press Enter to continue")

            manager.graph_topology_get(graph_topology.name)
            manager.invoke_wait_for_input("Press Enter to continue")

            manager.graph_instance_set(graph_instance)
            manager.invoke_wait_for_input("Press Enter to continue")

            manager.graph_instance_activate(graph_instance.name)
            manager.graph_instance_list()
            manager.invoke_wait_for_input("The graph instance has been activated. Press Enter to continue and deactivate the graph instance.")

            manager.graph_instance_deactivate(graph_instance.name)
            manager.graph_instance_delete(graph_instance.name)
            manager.graph_topology_delete(graph_topology.name)

        except Exception as ex:
            print(ex)