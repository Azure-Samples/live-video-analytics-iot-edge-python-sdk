import logging
from azure.media.analyticsedge import *

"""
Helper class for building a Motion detection graph topology
"""
class MotionDetectionTopology:
    
    def __init__(self):
        self.graph_topology_description = "Analyzing live video to detect motion and emit events"
        self.graph_topology_name = "MotionDetection"

    def build(self):
        graph_properties = MediaGraphTopologyProperties()
        graph_properties.description = self.graph_topology_description

        # Parameters
        user_name_param = MediaGraphParameterDeclaration(name="rtspUserName", type=MediaGraphParameterType.STRING, description="rtsp source user name.", default="testusername")
        password_param = MediaGraphParameterDeclaration(name="rtspPassword", type=MediaGraphParameterType.STRING, description="rtsp source password.", default="testpassword")
        url_param = MediaGraphParameterDeclaration(name="rtspUrl", type=MediaGraphParameterType.STRING)
        motion_sensitivity = MediaGraphParameterDeclaration(name="motionSensitivity", type=MediaGraphParameterType.STRING, description="motion detection sensitivity", default="medium")

        # Sources
        source = MediaGraphRtspSource(name="rtspSource", endpoint=MediaGraphUnsecuredEndpoint(url="${rtspUrl}", credentials=MediaGraphUsernamePasswordCredentials(username="${rtspUserName}", password="${rtspPassword}")))
        node_rtspSource = MediaGraphNodeInput(node_name="rtspSource")

        # Processors
        motion_processor = MediaGraphMotionDetectionProcessor(name="motionDetection", inputs=[node_rtspSource], sensitivity="${motionSensitivity}")

        # Sinks
        motion_detection_node = MediaGraphNodeInput(node_name="motionDetection")
        sink = MediaGraphIoTHubMessageSink(name="hubSink", inputs=[motion_detection_node], 
                hub_output_name="inferenceOutput")
        
        graph_properties.parameters = [user_name_param, password_param, url_param, motion_sensitivity]
        graph_properties.sources = [source]
        graph_properties.processors = [motion_processor]
        graph_properties.sinks = [sink]
        
        graph = MediaGraphTopology(name=self.graph_topology_name, properties=graph_properties)

        return graph
