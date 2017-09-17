import numpy as np
import pywt

from VideoAnalysis.get_stream_from_video import HandleStream

previous_flows = [0]*MAX_FLOWS


def preprocessing_data(stream, previous_flows):
    flows = stream.get_flow()
    previous_flows = previous_flows[0:len(flows)]
    return [data.append({'index': i, 'euclidean': np.linalg.norm(previous_flows - flows)}) for i in range(len(flows))], flows




