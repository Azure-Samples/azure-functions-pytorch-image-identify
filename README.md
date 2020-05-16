---
page_type: sample
languages:
- python
products:
- azure-functions
description: "This sample and walk-through deploys a Python Azure Function app for a machine learning scenario "
---

:construction: This is still under development! :construction:

## Azure Functions Python Machine Learning example (showing usage of Remote Build and Bring your own Storage)

<!-- 
Guidelines on README format: https://review.docs.microsoft.com/help/onboard/admin/samples/concepts/readme-template?branch=master

Guidance on onboarding samples to docs.microsoft.com/samples: https://review.docs.microsoft.com/help/onboard/admin/samples/process/onboarding?branch=master

Taxonomies for products and languages: https://review.docs.microsoft.com/new-hope/information-architecture/metadata/taxonomies?branch=master
-->

This sample shows how to set up, write and deploy a Python Machine Learning inference Azure Function app which uses Remote Build and Bring your own Storage features.

## Prerequisites

* [VSCode](https://code.visualstudio.com/) with the [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)   

* [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash)

* [Python installed locally](https://www.python.org/downloads/) 

* [Azure Account](https://azure.microsoft.com/en-us/free/) and access to [Azure Portal](https://azure.microsoft.com/en-us/features/azure-portal/) and [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest)

## Steps to set up and run locally

* Clone this repository using Git to a folder locally

* Open this directory in Visual Studio Code. Visual Studio Code should be able to recognize that this is a Function app and automatically activate the Azure Functions extension. See [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-python) for more.

* Start debugging using VSCode, you should see
    * PyTorch libraries downloaded locally (specified in the requirements.txt file)
    * The default PyTorch model "resnet18" is downloaded
    * The function app starts to run
    
    ![function-starts](https://raw.githubusercontent.com/anirudhgarg/functions-imageidentify/master/media/local-debugging.png)

    * Open a browser and invoke the function app with the URL to an image of an animal
    http://localhost:7071/api/classify?img=https://raw.githubusercontent.com/Azure-Samples/functions-python-pytorch-tutorial/master/resources/assets/penguin.jpg

    * You should see the following result
    ![result-local-debugging](https://raw.githubusercontent.com/anirudhgarg/functions-imageidentify/master/media/result-local-debugging.png)

### Update the code 

* Change the code in kafka_example.cs to point to your Kafka cluster that you set up in the previous step
```c#
public static class kafka_example
    {
        [FunctionName("kafkaApp")]
        public static void ConfluentCloudStringTrigger(
             [KafkaTrigger(
                "BootstrapServer",
                "users",
                ConsumerGroup = "<ConsumerGroup>",
                Protocol = BrokerProtocol.SaslSsl,
                AuthenticationMode = BrokerAuthenticationMode.Plain,
                Username = "<APIKey>",
                Password = "<APISecret>",
                SslCaLocation = "confluent_cloud_cacert.pem")]
        KafkaEventData<string> kafkaEvent,
        ILogger logger)
        {	    
            logger.LogInformation(kafkaEvent.Value.ToString());
        }
    }
```
  

### Running the sample

### Deploying the sample to a Azure Functions Premium Plan

### Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
