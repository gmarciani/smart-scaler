from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


IMAGES = dict(
  cyclic='gmarciani/smartscaler_cyclic'
)


class Controller(BaseHTTPRequestHandler):

  def sync(self, parent, children):
    parent_status = self.determine_status(children)

    smartscaler_name = parent['metadata']['name']
    smartscaler_spec = parent.get('spec', {})

    desired_pods = [self.build_pod(smartscaler_name, smartscaler_spec)]

    return dict(status=parent_status, children=desired_pods)

  def finalize(self, children):
    parent_status = self.determine_status(children)

    desired_pods = []

    finalized = len(children['Pod.v1']) == 0

    return dict(status=parent_status, children=desired_pods, finalized=finalized)

  def determine_status(self, children):
    return dict(pods=len(children['Pod.v1']))

  def build_pod(self, name, spec):
    return {
      'apiVersion': 'v1',
      'kind': 'Pod',
      'metadata': {
        'name': name
      },
      'spec': {
        'restartPolicy': 'OnFailure',
        'containers': [
          {
            'name': name,
            'image': IMAGES[spec['algorithm'].lower()],
            'env': [
              {'name': 'SMARTSCALER_DEPLOYMENT', 'value': str(spec['deployment'])},
              {'name': 'SMARTSCALER_ALGORITHM', 'value': str(spec['algorithm'])},
              {'name': 'SMARTSCALER_PARAMETERS', 'value': json.dumps(spec['parameters'])},
              {'name': 'SMARTSCALER_MIN_REPLICAS', 'value': str(spec['minReplicas'])},
              {'name': 'SMARTSCALER_MAX_REPLICAS', 'value': str(spec['maxReplicas'])}
            ]
          }
        ]
      }
    }

  def response(self, result):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(result))

  def do_POST(self):
    observed = json.loads(self.rfile.read(int(self.headers.getheader('content-length'))))

    parent = observed['parent']
    children = observed['children']
    finalizing = observed['finalizing']

    if finalizing is True:
      result = self.finalize(children)
    else:
      result = self.sync(parent, children)

    print('Smart Scaler response: %s' % result)

    self.response(result)


HTTPServer(('', 80), Controller).serve_forever()