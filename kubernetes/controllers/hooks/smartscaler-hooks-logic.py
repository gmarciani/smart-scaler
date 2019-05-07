from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class Controller(BaseHTTPRequestHandler):

  def sync(self, parent, children):
    print("Smart Scaler sync")

    parent_status = self.determine_status(children)

    smartscaler_name = parent["metadata"]["name"]
    smartscaler_spec = parent.get("spec", {})

    desired_pods = [self.build_pod(smartscaler_name, smartscaler_spec)]

    return dict(status=parent_status, children=desired_pods)


  def finalize(self, children):
    print("Smart Scaler finalize")

    parent_status = self.determine_status(children)

    desired_pods = []

    finalized = len(children["Pod.v1"]) == 0

    return dict(status=parent_status, children=desired_pods, finalized=finalized)


  def determine_status(self, children):
    return dict(pods=len(children["Pod.v1"]))


  def build_pod(self, name, spec):
    container = dict()
    container['name'] = 'smartscaler_cyclic'
    container['image'] = 'gmarciani/smartscaler_cyclic:latest'
    container['env'] = [
      dict(name='SMARTSCALER_DEPLOYMENT', value=spec['deployment']),
      dict(name='SMARTSCALER_PARAMETERS', value=json.dumps(spec['parameters'])),
      dict(name='SMARTSCALER_MIN_REPLICAS', value=spec['minReplicas']),
      dict(name='SMARTSCALER_MAX_REPLICAS', value=spec['maxReplicas'])
    ]

    pod = dict()
    pod['apiVersion'] = 'v1'
    pod['kind'] = 'Pod'
    pod['metadata'] = dict()
    pod['metadata']['name'] = name
    pod['spec'] = dict()
    pod['spec']['restartPolicy'] = 'OnFailure'
    pod['spec']['containers'] = [container]

    return pod


  def response(self, result):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(result))


  def do_POST(self):
    observed = json.loads(self.rfile.read(int(self.headers.getheader("content-length"))))

    parent = observed["parent"]
    children = observed["children"]
    finalizing = observed["finalizing"]

    if finalizing is True:
      result = self.finalize(children)
    else:
      result = self.sync(parent, children)

    print("Smart Scaler response: %s" % result)

    self.response(result)


HTTPServer(("", 80), Controller).serve_forever()