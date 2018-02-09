# Smart Scaler

*A smart auto-scaling service for Kubernetes, leveraging Reinforcement Learning*


## Build
The service is containerized with Docker, running:

    $> bash docker.sh


## Deploy
The service can be deployed in the following modes:


The deloyment can be executed, running:
    
    $> bash up.sh [MODE] [SERVICE]
    
where 
*[MODE]* is one of the following deployment modes:
* local: 
* kubernetes:

*[SERVICE]* is one of the following microservices:
* api_gateway
* agents_manager
* redis_simulator
* kubernetes_simulator

For example, to launch the API Gateway locally, run:

    $> bash up.sh local api_gateway


## Authors
Giacomo Marciani, [gmarciani@acm.org](mailto:gmarciani@acm.org)


## References
* "Smart elasticity for Kubernetes, leveraging reinforcement learning", 2018, G. Marciani


## License
The project is released under the [MIT License](https://opensource.org/licenses/MIT).
