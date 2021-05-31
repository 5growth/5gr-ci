### Project information
5GROWTH is funded by the European Union’s Research and Innovation Programme Horizon 2020 under Grant Agreement no. 856709


Call: H2020-ICT-2019. Topic: ICT-19-2019. Type of action: RIA. Duration: 30 Months. Start date: 1/6/2019


<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg" width="100px" />
</p>

<p align="center">
<img src="https://5g-ppp.eu/wp-content/uploads/2019/06/5Growth_rgb_horizontal.png" width="300px" />
</p>
 

# 5Growth CI/CD 

Main goals of the 5Growth CI/CD in the project are:

* Suppotrt software development;
* Create deployment automation for 5Growth platform;
* Create all-in-one environment for development experiments and familiarization with the platform.

Software development support explained in [architecture and workflow file](docs/architecture.md).

Deployment automation for 5Growth platform explained in [5growth platform deployment file](docs/containerization.md).

All-in-one environment described in [developer's environment file](docs/platform deployment.md)


### 5Growth CI/CD 

The CI/CD – is a software development concept and a set of practices targeted to automate and simplify the software development and deployment procedures. The 5Growth CI/CD, consists of two parts – Continuous Integration (CI) responsible for automated testing of a new code, and Continuous Deployment (CD) responsible for simple, repeatable, and reliable deployment. 5Growth CI/CD is built around and uses repositories, compute resources and network infrastructure of the project and integrated into it. For more details regarding 5Growth CI/CD, its architecture, flows and infrastructure please refer to D2.3 [1] section 3.3.2. 

High-level representation is described on Figure 12. 

<p align="center">
<img src="docs/img/Arch%20cicd%20straight(one%20piece).png"/>
</p>
<p align="center">
Figure 12 5Growth CI/CD architecture
</p>

5Growth CI/CD cycle allows to reduce time and resources, required for 5Growth platform deployment. 5Growth evaluation in detail can be found in section 4 D2.3 [1]. CD also able to ship entire 5Growth platform as a whole.



## Final release features

This table summarizes 5Growth CI/CD release 2 features. Release 1 was concentrated around creating core of CI/CD, main Jobs and Pipeline’s skeletons. Release 2 is mostly concentrating on options extension and deepening functionality, like extending test coverage, parametrizing deployment, extending infrastructure interactions.

<table>
  <tr>
   <td>Example
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Containerization: 
<ul>
<li>5Growth component containerization (Docker) 
</li>
</ul>
   </td>
   <td><strong>Containerization</strong>: 
<ul>
<li>Containerization extension to Kubernetes deployment 
</li>
</ul>
   </td>
   <td>
<ul>
<li>
</li>
</ul>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Environment management: 
<ul>
<li>Reworked LCM pipeline for environment management 
</li>
</ul>
   </td>
   <td><strong>Environment management:</strong>
<ul>
<li>Standardized developer's environment (minikube on top of devstack) 
<li>Infrastructure as Code approach for describing environments (develop, testbed, demo) 
<li>Automation for Kubernetes deployment
</li>
</ul>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>QA: 
<ul>
<li>Automated testing pipeline
</li>
</ul>
   </td>
   <td><strong>QA:</strong>
<ul>
<li>Extend testing
</li>
</ul>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>


## Containerization
In release 2 CI/CD framework was extended with advanced containerization capabilities. Previously containerized platform is now adapted for Kubernetes deployment. This allowed to significantly reduce deployment time but required infrastructure extension and deployment process adaptation. New continuous integration Pipelines now is able to store validated images in a docker registry. 5Tonic environment was extended with a docker registry and Kubernetes cluster. There were new deployment Pipelines developed for Kubernetes. Deployment process for Kubernetes requires different approach in 5Growth platform components configuration and interactions.
## Environment management
Stable and repeatable environment is crucial for development and deployment processes automation. Environment repeatability is achieved via Infrastructure as Code (IaC) approach. IaC is implemented in testbeds for platform code validation, for platform deployment and specially designed for development environment, that may be automatically deployed on developer’s workstation. For all these purposes were developed automation able to deploy similar environments regardless of where and for what purpose it would be used.
## QA
In a code validation phase automated tests checks code functionality, regression and integration perspectives and deployment readiness.