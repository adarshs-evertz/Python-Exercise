"""Pre and post traffic lambda deploy hooks."""
import boto3

codedeploy = boto3.client("codedeploy")

# EVENT
DEPLOYMENT_ID = "DeploymentId"
LIFECYCLE_EVENT_ID = "LifecycleEventHookExecutionId"


# pylint: disable=unused-argument
def get_item_pre_traffic_hook(event, context):
    """
    Run Pre Traffic Deploy Hook.

    :param event: CodeDeploy Event
    :param context: Lambda Invocation Context
    """
    deployment_id = event.get(DEPLOYMENT_ID)
    lifecycle_event_id = event.get(LIFECYCLE_EVENT_ID)
    status = "Succeeded"

    # pylint: disable=unused-variable
    codedeploy_response = codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_id,
        status=status,
    )


# pylint: disable=unused-argument
def get_item_post_traffic_hook(event, context):
    """
    Run Post Traffic Deploy Hook.

    :param event: CodeDeploy Event
    :param context: Lambda Invocation Context
    """
    deployment_id = event.get(DEPLOYMENT_ID)
    lifecycle_event_id = event.get(LIFECYCLE_EVENT_ID)
    status = "Succeeded"

    # pylint: disable=unused-variable
    codedeploy_response = codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_id,
        status=status,
    )
