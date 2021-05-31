# 5Growth platform containerization
The containerization approach allows 5Growth platform deployment regardless of the OS.

5Growth platform deployment described in docker-compose file and require docker and docker-compose installed.

Platform containerization allows to deploy folloving platform components:
* 5Gr-VS;
* 5Gr-SO;
* 5Gr-RL;
* 5Gr-VoMS


Containerization files are in the containerization folder. Every containerized component is placed in a correspondent subfolder.
Every subfolder contains:
* platform configuration files;
* quality assurance tests;
* docker deployment files and bash scripts.

## Platform configuration files
Platform configuration files are component- and environment-specific. Every component requires access to one or a few different components e.g. IP addresses or DNS names. Service Orchestrator requires access to external MANO (Cloudify, OSM), Resource Layer requires authorization to external OpenStack, etc. Configuration descriptions can be found in a correspondent component repository.    

## Quality assurance tests
QA was used for development support in CI workflow. CI workflow described in more detail in [architecture and workflow file](docs/architecture.md).

## Docker deployment files and bash scripts
The containerization framework was developed to simplify 5Growth platform deployment to arbitrary nodes. That's why it allows to download platform source code from public repositories and build every platform component. For building components Dockerfile is responsible.

Deployment described and controlled by docker-compose file. To execute these files start the deployment process docker and docker-compose are required.


# 5Growth platform deployment
To deploy platform:
1. clone CI repository
```
git clone https://github.com/5growth/5gr-ci
```
2. change to containerization directory
```
cd 5gr-ci/containerization
```
3. choose and change to a component subdirectory, e.g so
```
cd 5gr-ci/containerization/so
```
4. configure component
5. run a bash script
```
./so_build_docker.sh
```