import json
from kubernetes import client, config
from kubernetes.client import configuration
from prometheus_http_client import Prometheus
import os
import time
import sys

def get_deployment_data(cluster, deployment, namespace):
    config.load_kube_config(context=cluster)
    api = client.ExtensionsV1beta1Api()
    api_response = api.read_namespaced_deployment_status(deployment, namespace, _preload_content=False)
    json_data = api_response.read()
    deploy_dict = json.loads(json_data.decode('utf-8'))
    return deploy_dict

def main():

    cluster = os.getenv('CLUSTER')
    deployment = os.getenv('DEPLOYMENT')
    deploy_timeout = os.getenv('DEPLOY_TIMEOUT')
    namespace = os.getenv('NAMESPACE')
    testing_time_total = os.getenv('TOTAL')
    testing_time_wait = os.getenv('WAIT')
    threshold = os.getenv('THRESHOLD')

    timeout = time.time() + int(deploy_timeout)

    deployment_completed = False
    while not deployment_completed:
        try:
            deployment_dict = get_deployment_data(cluster, deployment, namespace)
            unavailable_replicas = deployment_dict['status']['unavailableReplicas']
            print('Deployment has not completed...')
            print(f'Deployment has {unavailable_replicas} unavailable replicas.')
            time.sleep(int(testing_time_wait))
            if time.time() > timeout:
                print(f'Deployment Timeout ({deploy_timeout}) Exceeded!' )
                print('Rollback Initiated')
                sys.exit(1)
        except:
            deployment_completed = True
            print('Deployment Completed Successfully')
            pass

    # Prometheus Tests

    prometheus = Prometheus()

    app_info = f'namespace="{namespace}", deployment="{deployment}"'

    metric = 'sum(irate(response_total{classification="success", %s, direction="inbound"}[30s])) / sum(irate(response_total{%s, direction="inbound"}[30s]))' % (app_info, app_info)

    t_end = time.time() + int(testing_time_total)

    while time.time() < t_end:
        success_metrics_available = False
        while not success_metrics_available:
            try:
                query_results = prometheus.query(metric=f'{metric}')
                query_dict = json.loads(query_results)
                success_percent = query_dict['data']['result'][0]['value'][1]
                if success_percent.replace('.','',1).isdigit():
                    print('Success Metrics Available...')
                    success_metrics_available = True
                else:
                    print('Success Metrics Not Yet Available...')
                    if time.time() > t_end:
                        print(f'Testing Timeout ({deploy_timeout}) Exceeded!' )
                        print('Rollback Initiated')
                        sys.exit(1)
                    time.sleep(int(testing_time_wait))
            except:
                print('Success Metrics Not Yet Available...')
                if time.time() > t_end:
                    print(f'Testing Timeout ({deploy_timeout}) Exceeded!' )
                    print('Rollback Initiated')
                    sys.exit(1)
                time.sleep(int(testing_time_wait))
                pass

        if float(success_percent) >= float(threshold):
            print('Everything is awesome!!!')
            time.sleep(int(testing_time_wait))
        else:
            print(f'Success Rate {success_percent} lower than threshold')
            print('Rollback Initiated')
            sys.exit(1)

if __name__ == "__main__":
    main()