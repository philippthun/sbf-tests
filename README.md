### General preparation

Login to CF and target an org/space where test services can be created and test apps can be deployed. The `diego_docker` and `diego_cnb` feature flags must be enabled.

Create a user-provided service:
```
cf create-user-provided-service upsi -p '{"username":"admin","password":"pa55woRD"}' -t "list, of, tags"
```

### Buildpack app

#### Preparation

Create a test app, enable file-based service bindings, bind the user-provided service and push the app.
```
cf create-app sbf-test-bp

cf curl -X PATCH "/v3/apps/$(cf app sbf-test-bp --guid)/features/file-based-service-bindings" -d '{ "enabled": true }'

cf bind-service sbf-test-bp upsi

cf push sbf-test-bp
```

#### Check env var and files in container via ssh

```
cf ssh sbf-test-bp -c 'find $SERVICE_BINDING_ROOT -type f -exec bash -c "echo {}: \$(cat {})" \;'

/etc/cf-service-bindings/upsi/provider: user-provided
/etc/cf-service-bindings/upsi/type: user-provided
/etc/cf-service-bindings/upsi/binding-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/instance-name: upsi
/etc/cf-service-bindings/upsi/instance-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/tags: ["list","of","tags"]
/etc/cf-service-bindings/upsi/name: upsi
/etc/cf-service-bindings/upsi/label: user-provided
/etc/cf-service-bindings/upsi/username: admin
/etc/cf-service-bindings/upsi/password: pa55woRD
```

#### Check env var and files in app process via curl

```
curl $(cf curl "/v3/apps/$(cf app sbf-test-bp --guid)/routes" | jq -r ".resources[].url")?plain=true

/etc/cf-service-bindings/upsi/provider: user-provided
/etc/cf-service-bindings/upsi/type: user-provided
/etc/cf-service-bindings/upsi/binding-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/instance-name: upsi
/etc/cf-service-bindings/upsi/instance-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/tags: ["list","of","tags"]
/etc/cf-service-bindings/upsi/name: upsi
/etc/cf-service-bindings/upsi/label: user-provided
/etc/cf-service-bindings/upsi/username: admin
/etc/cf-service-bindings/upsi/password: pa55woRD
```

#### Check env var and files in sidecar via recent logs

```
cf logs sbf-test-bp --recent | grep -o '\[.*/SIDECAR/.*'

[...]
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/provider: user-provided
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/type: user-provided
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/binding-guid: 00000000-0000-0000-0000-000000000000
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/instance-name: upsi
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/instance-guid: 00000000-0000-0000-0000-000000000000
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/tags: ["list","of","tags"]
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/name: upsi
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/label: user-provided
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/username: admin
[APP/PROC/WEB/SIDECAR/SIDECAR/0] OUT /etc/cf-service-bindings/upsi/password: pa55woRD
[...]
```

#### Check env var and files in task via recent logs

```
cf run-task sbf-test-bp --command "./task.sh" --name task

cf logs sbf-test-bp --recent | grep -o '\[.*/TASK/.*'

[...]
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/provider: user-provided
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/type: user-provided
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/binding-guid: 00000000-0000-0000-0000-000000000000
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/instance-name: upsi
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/instance-guid: 00000000-0000-0000-0000-000000000000
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/tags: ["list","of","tags"]
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/name: upsi
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/label: user-provided
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/username: admin
[APP/TASK/task/0] OUT /etc/cf-service-bindings/upsi/password: pa55woRD
[...]
```

#### Check env var and files during staging

```
cf push sbf-test-bp -p staging

[...]
Exception: /etc/cf-service-bindings/upsi/provider: user-provided
/etc/cf-service-bindings/upsi/type: user-provided
/etc/cf-service-bindings/upsi/binding-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/instance-name: upsi
/etc/cf-service-bindings/upsi/instance-guid: 00000000-0000-0000-0000-000000000000
/etc/cf-service-bindings/upsi/tags: ["list","of","tags"]
/etc/cf-service-bindings/upsi/name: upsi
/etc/cf-service-bindings/upsi/label: user-provided
/etc/cf-service-bindings/upsi/username: admin
/etc/cf-service-bindings/upsi/password: pa55woRD
[...]
```

### Docker app

A Docker image has been build from this repository and pushed to Docker Hub:

```
docker build --platform linux/amd64 -t philippthun693/sbf-tests .

docker push philippthun693/sbf-tests
```

#### Preparation

Create a test app, enable file-based service bindings, bind the user-provided service and push the app.
```
cf create-app sbf-test-dk --app-type docker

cf curl -X PATCH "/v3/apps/$(cf app sbf-test-dk --guid)/features/file-based-service-bindings" -d '{ "enabled": true }'

cf bind-service sbf-test-dk upsi

cf push sbf-test-dk -f manifest-docker.yml
```

#### Check env var and files in container via ssh

```
cf ssh sbf-test-dk -c 'find $SERVICE_BINDING_ROOT -type f -exec bash -c "echo {}: \$(cat {})" \;'

[... same output as above ...]
```

#### Check env var and files in app process via curl

```
curl $(cf curl "/v3/apps/$(cf app sbf-test-dk --guid)/routes" | jq -r ".resources[].url")?plain=true

[... same output as above ...]
```

#### Check env var and files in sidecar via recent logs

```
cf logs sbf-test-dk --recent | grep -o '\[.*/SIDECAR/.*'

[... same output as above ...]
```

#### Check env var and files in task via recent logs

```
cf run-task sbf-test-dk --command "./task.sh" --name task

cf logs sbf-test-dk --recent | grep -o '\[.*/TASK/.*'

[... same output as above ...]
```

#### Check env var and files during staging

For Docker apps there is no staging process involving user-provided code.

### CNB app

#### Preparation

Push a test app, enable file-based service bindings, bind the user-provided service and restage the app.
```
cf push sbf-test-cnb -f manifest-cnb.yml

cf curl -X PATCH "/v3/apps/$(cf app sbf-test-cnb --guid)/features/file-based-service-bindings" -d '{ "enabled": true }'

cf bind-service sbf-test-cnb upsi

cf restage sbf-test-cnb
```

#### Check env var and files in container via ssh

```
cf ssh sbf-test-cnb -c 'find $SERVICE_BINDING_ROOT -type f -exec bash -c "echo {}: \$(cat {})" \;'

[... same output as above ...]
```

#### Check env var and files in app process via curl

```
curl $(cf curl "/v3/apps/$(cf app sbf-test-cnb --guid)/routes" | jq -r ".resources[].url")?plain=true

[... same output as above ...]
```

#### Check env var and files in sidecar via recent logs

Currently not working...

#### Check env var and files in task via recent logs

```
cf run-task sbf-test-cnb --command "./task.sh" --name task

cf logs sbf-test-cnb --recent | grep -o '\[.*/TASK/.*'

[... same output as above ...]
```

#### Check env var and files during staging

```
cf push sbf-test-cnb -f manifest-cnb.yml -p staging

[... same output as above ...]
```
