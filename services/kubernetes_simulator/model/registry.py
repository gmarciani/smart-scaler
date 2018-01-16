"""
Simulation of Kubernetes registry.
"""


SMART_SCALERS = {}  # the registry of Smart Scalers {smart_scaler_name: SmartScaler}

PODS_DB = {}  # the dictionary of Pods {pod_name: Pod}