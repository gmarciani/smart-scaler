# Smart Scaler

*A smart scaler for Kubernetes*


## Build
Install all required packages with PIP, running:

    $> pip install -r requirements.txt


## Simulations
Demule provides the user with the following simulation models:

* cloud: a simulation about Cloud computing

Launch a simulation, running:

    $> python simulation.py [MY_SIMULATION] --config [MY_CONFIGURATION]
    
where 
*[MY_SIMULATION]* is the name of the simulation to launch, i.e. the package name contained in demule.simulations, and
*[MY_CONFIGURATION]* is the relative path to the YAML configuration file for the simulation.

For example, to launch the cloud simulation, run:

    $> python simulation.py cloud --config simulations/cloud/sample.yaml


### Configuration
We state here a sample configuration, that is the one specified by *experiments/cloud/simulation.yaml*:

```yaml
general:
  t_stop: 50000
  replica: 3
  random:
    generator: "MarcianiMultiStream"
    seed: 123456789
cloudlet:
  n_servers: 20
cloud:
  t_service_rate_1: 0.75
  t_service_rate_2: 0.85
  t_setup: 95
```

## Authors
Giacomo Marciani, [gmarciani@acm.org](mailto:gmarciani@acm.org)


## References
* "Discrete-Event Simulation", 2006, L.M. Leemis, S.K. Park
* "Performance Modeling and Design of Computer Systems, 2013, M. Harchol-Balter


## License
The project is released under the [MIT License](https://opensource.org/licenses/MIT).
