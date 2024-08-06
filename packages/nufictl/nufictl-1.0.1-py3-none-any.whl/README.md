### Python CLI (name : nufictl) for CRD npudeploy 

```bash
poetry shell
poetry install
```

* nufictl exmaple
```bash
nufictl ls

(nufi-cli-py3.12) kade93-mac-air-m2 :: workspaces/aichip/nufi-cli ‹feature/nufi-cli*› % nufictl ls                                                                       
+---------------------------+---------------------------+----------+---------------------+---------------------------------------------------+
|           Name            |         Namespace         | Replicas |       Created       |                   Endpoint URL                    |
+---------------------------+---------------------------+----------+---------------------+---------------------------------------------------+
| npu-deploy-nginx-hxyvjbwr | kubeflow-user-example-com |    1     | 2024-08-05 06:48:04 |   https://[npu-deploy-url].com:4443               |
|   test-npu-deploy-cli-0   | kubeflow-user-example-com |    1     | 2024-08-05 06:31:05 |   https://test-npu-deploy-cli-0.com:4443          |
+---------------------------+---------------------------+----------+---------------------+---------------------------------------------------+

nufictl create

Name [npu-deploy-example]: nufictl-test
Image [nginx]: 
CPU [1]: 
Memory [1]: 
Replicas [1]: 
Accelerator Type [npu]: 
Accelerator Count [1]: 
Successfully created nufictl-test with image: nginx


nufictl run --image=nginx                                                        
Successfully created npu-deploy-nginx-70w2c8yt with image: nginx


nufictl delete npu-deploy-example                                           
Successfully deleted npu-deploy-example
```