import logging
from azure.media.analyticsedge import *

"""
Helper class for building a Continuous video recording graph topology
"""
class CvrTopology:
    
    def __init__(self):
        self.graph_topology_description = "Continuous video recording to an Azure Media Services Asset"
        self.graph_topology_name = "ContinuousRecording"

    def build(self):
        graph_properties = MediaGraphTopologyProperties()
        graph_properties.description = self.graph_topology_description

        # Parameters
        user_name_param = MediaGraphParameterDeclaration(name="rtspUserName", type=MediaGraphParameterType.STRING, default="testusername")
        password_param = MediaGraphParameterDeclaration(name="rtspPassword", type=MediaGraphParameterType.STRING, default="testpassword")
        url_param = MediaGraphParameterDeclaration(name="rtspUrl", type=MediaGraphParameterType.STRING)

        # Sources
        source = MediaGraphRtspSource(name="rtspSource", endpoint=MediaGraphUnsecuredEndpoint(url="${rtspUrl}", credentials=MediaGraphUsernamePasswordCredentials(username="${rtspUserName}", password="${rtspPassword}")))
        node = MediaGraphNodeInput(node_name="rtspSource")
        
        # Sinks
        sink = MediaGraphAssetSink(name="assetsink", inputs=[node], 
                asset_name_pattern='sampleAsset-${System.GraphTopologyName}-${System.GraphInstanceName}', 
                segment_length="PT0H0M30S", local_media_cache_maximum_size_mi_b=2048, local_media_cache_path="/var/lib/azuremediaservices/tmp/")
        
        graph_properties.parameters = [user_name_param, password_param, url_param]
        graph_properties.sources = [source]
        graph_properties.sinks = [sink]
        
        graph = MediaGraphTopology(name=self.graph_topology_name, properties=graph_properties)
        
        return graph
