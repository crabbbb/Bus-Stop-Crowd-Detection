import numpy as np

def serializeBusCentroid(busCentroid):
    '''
    Convert busCentroid dictionary into JSON-serializable format.
    busCentroid = {
        busId: {
            "centroid": np.array([x, y]),
            "numberMatch": int,
            "station": str or None,
            "status": BusStatus (enum)
        }
    }
    '''
    output = {}
    for bus_id, info in busCentroid.items():
        # Convert the centroid np.array to a Python list
        centroidList = info["centroid"].tolist() if isinstance(info["centroid"], np.ndarray) else info["centroid"]

        # Convert enum to string
        statusStr = str(info["status"])  # or info["status"].value

        output[bus_id] = {
            "centroid": centroidList,
            "numberMatch": info["numberMatch"],
            "station": info["station"],
            "status": statusStr
        }
    return output
