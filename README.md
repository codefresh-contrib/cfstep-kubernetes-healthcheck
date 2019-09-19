# cfstep-linkerd-healthcheck

Prometheus Health Check Query based on Linkerd Success Percentage

Types:
`kubernetes` Check that Kubernetes deployment has all replicas available (Deployment Successful)
`linkerd` Watch Prometheus metrics from Linkerd for given time confirming Success Rate remains higher than threshold configured.

If either of the above fail the step will fail accordingly

| ENVIRONMENT VARIABLE | DEFAULT | TYPE | REQUIRED | DESCRIPTION |
|----------------------------|----------|---------|----------|---------------------------------------------------------------------------------------------------------------------------------|
| CLUSTER | null | string | No | Required for Kubernetes Type / Kubernetes Context Name |
| DEPLOY_TIMEOUT | null | integer | No | (seconds) Required for Kubernetes Type / Timeout for Deployment Completion |
| DEPLOYMENT | null | string | Yes | Kubernetes Deployment Name |
| KUBE_CONFIG | null | string | Yes | Location of Kube Config file |
| METRIC_TIMEOUT | null | integer | No | (seconds) Required for Linkerd Type / Time to wait for Prometheus to return metrics |
| NAMESPACE | null | string | Yes | Kubernetes Namespace of Deployment |
| PROMETHEUS_URL | null | string | Yes | Prometheus URL including protocol and port |
| THRESHOLD | null | integer | No | Required for Linkerd Type / Percentage represented in 1 - .01 (100% - 1%) |
| TOTAL | null | integer | No | (seconds) Required for Linkerd Type / Total Time to Continue Testing |
| TYPES | null | string | Yes | Type of Tests to Run |
| WAIT | null | integer | Yes | (seconds) Wait between tests |

Example Step Usage:

``` yaml
  CheckDeploymentHealth:
    title: Checking Deployment Health...
    image: dustinvanbuskirk/cfstep-healthcheck:alpha
    environment:
      - TYPES=kubernetes,linkerd
      - CLUSTER=sales-demo@FirstKubernetes
      - DEPLOY_TIMEOUT=120
      - DEPLOYMENT=example-voting-app-vote
      - KUBE_CONFIG=/codefresh/volume/sensitive/.kube/config
      - METRIC_TIMEOUT=120
      - NAMESPACE=dustinvb-staging
      - PROMETHEUS_URL=http://10.59.254.185:9090
      - THRESHOLD=1
      - TOTAL=90
      - WAIT=15
```