import logging
from azure.media.analyticsedge import *

"""
Helper class for building an Event-based video recording graph topology
"""
class Evr:
    
    def __init__(self):
        self.graph_topology_description = "Event - based video recording to local files based on motion events"
        self.graph_topology_name = "EventsToFilesMotionDetection"
        
    def build(self):
        graph_properties = MediaGraphTopologyProperties()
        graph_properties.description = self.graph_topology_description

        # Parameters
        user_name_param = MediaGraphParameterDeclaration(name="rtspUserName", type="String", description="rtsp source user name.", default="testusername")
        password_param = MediaGraphParameterDeclaration(name="rtspPassword", type="String", description="rtsp source password.", default="testpassword")
        url_param = MediaGraphParameterDeclaration(name="rtspUrl", type="String")
        motion_sensitivity = MediaGraphParameterDeclaration(name="motionSensitivity", type="String", description="motion detection sensitivity", default="medium")
        fileSinkOutputName = MediaGraphParameterDeclaration(name="fileSinkOutputName", type="String", description="file sink output name", default="filesinkOutput")

        # Sources
        source = MediaGraphRtspSource(name="rtspSource", endpoint=MediaGraphUnsecuredEndpoint(url="${rtspUrl}", credentials=MediaGraphUsernamePasswordCredentials(username="${rtspUserName}", password="${rtspPassword}")))
        node_rtspSource = MediaGraphNodeInput(node_name="rtspSource")

        # Processors
        motion_processor = MediaGraphMotionDetectionProcessor(name="motionDetection", inputs=[node_rtspSource], sensitivity="${motionSensitivity}")
        motion_node = MediaGraphNodeInput(node_name="motionDetection")
        signal_gate_processor = MediaGraphSignalGateProcessor(name="signalGateProcessor", inputs=[motion_node, node_rtspSource],
            activation_signal_offset="PT0S", minimum_activation_time="PT5S", maximum_activation_time="PT5S", activation_evaluation_window="PT1S")
        
        # Sinks
        signal_gate_node = MediaGraphNodeInput(node_name="signalGateProcessor")
        sink = MediaGraphFileSink(name="fileSink", inputs=[signal_gate_node], 
                file_name_pattern='sampleFilesFromEVR-${fileSinkOutputName}-${System.DateTime}', 
                base_directory_path="/var/media", maximum_size_mi_b=512)
        
        graph_properties.parameters = [user_name_param, password_param, url_param, motion_sensitivity, fileSinkOutputName]
        graph_properties.sources = [source]
        graph_properties.processors = [motion_processor, signal_gate_processor]
        graph_properties.sinks = [sink]
        
        graph = MediaGraphTopology(name=self.graph_topology_name, properties=graph_properties)

        return graph
