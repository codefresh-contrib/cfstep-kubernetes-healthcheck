# cfstep-linkerd-healthcheck

Prometheus Health Check Query based on Linkerd Success Percentage

Step will:
1. Check that Kubernetes deployment has all replicas available (Deployent Successful)
2. Watch Prometheus metrics from Linkerd for given time confirming Success Rate remains higher than threshold configured.

If either of the above fail the step will fail accordingly

| ENVIRONMENT VARIABLE | DEFAULT | TYPE | REQUIRED | DESCRIPTION |
|----------------------------|----------|---------|----------|---------------------------------------------------------------------------------------------------------------------------------|
| CLUSTER | null | string | Yes | Kubernetes Context Name |
| DEPLOY_TIMEOUT | null | integer | Yes | Timeout for Deployment Completion |
| DEPLOYMENT | null | string | Yes | Kubernetes Deployment Name |
| KUBE_CONFIG | null | string | Yes | Location of Kube Config file |
| NAMESPACE | null | string | Yes | Kubernetes Namespace of Deployment |
| PROMETHEUS_URL | null | string | Yes | Prometheus URL including protocol and port |
| THRESHOLD | null | integer | Yes | Percentage represented in 1 - .01 (100% - 1%) |
| TOTAL | null | integer | Yes | Total Time to Continue Testing |
| WAIT | null | integer | Yes | Wait between tests |

Example Step Usage:

``` yaml
  CheckDeploymentHealth:
    title: Checking Deployment Health...
    image: dustinvanbuskirk/cfstep-healthcheck:alpha
    environment:
      - CLUSTER=sales-demo@FirstKubernetes
      - DEPLOY_TIMEOUT=120
      - DEPLOYMENT=example-voting-app-vote
      - KUBE_CONFIG=/codefresh/volume/sensitive/.kube/config
      - NAMESPACE=dustinvb-staging
      - PROMETHEUS_URL=http://10.59.254.185:9090
      - THRESHOLD=1
      - TOTAL=90
      - WAIT=15
```