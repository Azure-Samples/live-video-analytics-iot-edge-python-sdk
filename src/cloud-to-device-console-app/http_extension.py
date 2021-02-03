from azure.media.analyticsedge import *
 
"""
Helper class for building an inferencing using HTTP extension and then, to an external module using IoT Hub routing capabilities
"""
class HttpExtensionTopology:
    
    def __init__(self):
        self.graph_topology_description = "Analyzing live video using HTTP Extension to send images to an external inference engine"
        self.graph_topology_name = "InferencingWithHttpExtension"
        
    def build(self):
        graph_properties = MediaGraphTopologyProperties()
        graph_properties.description = self.graph_topology_description

        # Parameters
        user_name_param = MediaGraphParameterDeclaration(name="rtspUserName", type=MediaGraphParameterType.STRING, description="rtsp source user name.", default="testusername")
        password_param = MediaGraphParameterDeclaration(name="rtspPassword", type=MediaGraphParameterType.STRING, description="rtsp source password.", default="testpassword")
        url_param = MediaGraphParameterDeclaration(name="rtspUrl", type=MediaGraphParameterType.STRING)
        hub_source_input = MediaGraphParameterDeclaration(name="hubSourceInput", type=MediaGraphParameterType.STRING, description="inferencing Url.", default="recordingTrigger")
        inferencing_url = MediaGraphParameterDeclaration(name="inferencingUrl", type=MediaGraphParameterType.STRING, description="file sink output name.", default="http://yolov3/score")
        inferencing_username = MediaGraphParameterDeclaration(name="inferencingUserName", type=MediaGraphParameterType.STRING, description="inferencing endpoint user name.", default="dummyUserName")
        inferencing_password = MediaGraphParameterDeclaration(name="inferencingPassword", type=MediaGraphParameterType.STRING, description="inferencing endpoint password.", default="dummyPassword")
        image_scale_mode = MediaGraphParameterDeclaration(name="imageScaleMode", type=MediaGraphParameterType.STRING, description="image scaling mode.", default="preserveAspectRatio")
        frame_width = MediaGraphParameterDeclaration(name="frameWidth", type=MediaGraphParameterType.STRING, description="width of the video frame to be received from LVA.", default="416")
        frame_height = MediaGraphParameterDeclaration(name="frameHeight", type=MediaGraphParameterType.STRING, description="height of the video frame to be received from LVA.", default="416")

        # Sources
        source = MediaGraphRtspSource(name="rtspSource", endpoint=MediaGraphUnsecuredEndpoint(url="${rtspUrl}", credentials=MediaGraphUsernamePasswordCredentials(username="${rtspUserName}", password="${rtspPassword}")))
        node_rtspSource = MediaGraphNodeInput(node_name="rtspSource")

        # Processors
        http_processor = MediaGraphHttpExtension(name="inferenceClient", inputs=[node_rtspSource], endpoint=MediaGraphUnsecuredEndpoint(url="${inferencingUrl}", credentials=MediaGraphUsernamePasswordCredentials(username="${inferencingUserName}", password="${inferencingPassword}")),
        image=MediaGraphImage(scale=MediaGraphImageScale(mode="${imageScaleMode}", width="${frameWidth}", height="${frameHeight}"), format=MediaGraphImageFormatBmp()))
                           
        # Sinks
        hub_graph_node = MediaGraphNodeInput(node_name="inferenceClient")
        sink = MediaGraphIoTHubMessageSink(name="hubSink", inputs=[hub_graph_node], 
                hub_output_name="inferenceOutput")

        graph_properties.parameters = [user_name_param, password_param, url_param, hub_source_input, inferencing_url, inferencing_username, inferencing_password, image_scale_mode, frame_height, frame_width ]
        graph_properties.sources = [source]
        graph_properties.processors = [http_processor]
        graph_properties.sinks = [sink]
        
        graph = MediaGraphTopology(name=self.graph_topology_name, properties=graph_properties)

        return graph
