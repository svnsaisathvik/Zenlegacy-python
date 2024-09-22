# 🚀 AWS Management Discord Bot 🌩️

This bot is designed to help users manage their AWS infrastructure
directly from a Discord server. It integrates AWS services like EC2,
RDS, DynamoDB, and Cost Explorer, offering a range of operations such as
instance management, cost optimization, incident response, and threat
monitoring. Additionally, the bot uses GPT-powered AI to suggest AWS
cost optimizations.

## 📑 Table of Contents

-   [Features](#features)
-   [Setup Instructions](#setup-instructions)
-   [Commands](#commands)
-   [AWS Helper Functions](#aws-helper-functions)
    -   [get_service_client](#get_service_client)
    -   [get_cost_for_service](#get_cost_for_service)
    -   [get_current_instance_count](#get_current_instance_count)
    -   [update_instance_count](#update_instance_count)
    -   [format_guardduty_findings](#format_guardduty_findings)
-   [Log Management](#log-management)
-   [Additional Notes](#additional-notes)

------------------------------------------------------------------------

## 🎯 Features

1.  **AWS Instance Management**: Start, stop, and terminate EC2, RDS,
    and DynamoDB instances.
2.  **💰 Cost Monitoring**: Get current usage costs of EC2, S3, RDS, and
    DynamoDB using AWS Cost Explorer.
3.  **🔐 Security Management**: Manage AWS IAM roles and monitor threats
    using AWS GuardDuty.
4.  **🔥 Incident Response**: A command to resolve incidents within AWS
    infrastructure.
5.  **🧠 GPT Integration**: Get AI-generated cost optimization
    suggestions based on current AWS usage.
6.  **📢 Discord Notifications**: Sends actionable notifications and
    real-time responses to user commands.

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### Prerequisites

1.  **Python 3.8+**

2.  **AWS Account** with permissions for EC2, RDS, DynamoDB, IAM,
    GuardDuty, and Cost Explorer.

3.  **Discord Bot**: Set up a Discord bot via the [Discord Developer
    Portal](https://discord.com/developers/applications).

4.  **Boto3**: AWS SDK for Python.

    ``` bash
    pip install boto3
    ```

5.  **OpenAI API Key** for GPT-powered suggestions (from
    [OpenAI](https://openai.com/api)).

6.  **Install `discord.py` for Discord Bot:**

    ``` bash
    pip install discord.py
    pip install openai
    ```

### Installation Steps

1.  Clone the repository:

    ``` bash
    git clone https://github.com/your-repo/aws-management-discord-bot.git
    cd aws-management-discord-bot
    ```

2.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Set up your `aws_credentials.json` file in the `config/` directory:

    ``` json
    {
        "aws_access_key": "your_access_key",
        "aws_secret_key": "your_secret_key",
        "region": "your_region"
    }
    ```

4.  Set up your `bot_config.json` file in the `config/` directory:

    ``` json
    {
        "discord_token": "your_discord_bot_token",
        "openai_api_key": "your_openai_api_key"
    }
    ```

5.  Run the bot:

    ``` bash
    python bot.py
    ```

------------------------------------------------------------------------

## 🎮 Commands

  ------------------------------------------------------------------------------
  Command                  Description
  ------------------------ -----------------------------------------------------
  `!scale_ec2`             Auto-scale EC2 instances based on load.

  `!optimize_costs`        💡 Get GPT-powered suggestions to optimize AWS costs.

  `!genai_advice`          🤖 Get AI advice on AWS service usage and future
                           recommendations.

  `!incident_resolution`   🚨 Resolve a simulated AWS incident.

  `!manage_iam`            🔐 Perform IAM actions (create, update, delete
                           roles).

  `!monitor_threats`       🔍 Monitor AWS GuardDuty for active threats and
                           vulnerabilities.

  `!manage_service`        🛠️ Manage EC2, RDS, and DynamoDB services
                           (start/stop/delete).
  ------------------------------------------------------------------------------

Each command provides feedback in Discord, often with emoji-based status
indicators (✅ for success, ❌ for failure).

------------------------------------------------------------------------

## 🛠️ AWS Helper Functions

### `get_service_client`

Returns a Boto3 client for a supported AWS service. If an unsupported
service is requested, it raises a `ValueError`.

``` python
def get_service_client(service_name):
    """Get a Boto3 client for the specified AWS service."""
    if service_name not in SUPPORTED_SERVICES:
        raise ValueError(f"Unsupported service: {service_name}")
    return boto3.client(service_name,
                        aws_access_key_id=aws_credentials['aws_access_key'],
                        aws_secret_access_key=aws_credentials['aws_secret_key'],
                        region_name=aws_credentials['region'])
```

### `get_cost_for_service`

Queries the AWS Cost Explorer to retrieve the costs for a specified
service.

``` python
def get_cost_for_service(service_name):
    """Retrieve the cost associated with a specific AWS service."""
```

### `get_current_instance_count`

Fetches the number of running instances (EC2, RDS, DynamoDB) and returns
the count along with instance details.

``` python
def get_current_instance_count(service_name):
    """Get the current instance count for EC2, RDS, or DynamoDB."""
```

### `update_instance_count`

Allows actions like starting, stopping, or terminating instances for
EC2, RDS, and DynamoDB.

``` python
def update_instance_count(service_name, action, instance_identifier=None):
    """Update the instance count by starting, stopping, or terminating instances."""
```

### `format_guardduty_findings`

Formats AWS GuardDuty findings for easier readability.

``` python
def format_guardduty_findings(findings):
    """Format GuardDuty findings for easier readability."""
```

------------------------------------------------------------------------

## 📝 Log Management

All actions are logged in `aws_service_actions.log` for auditing
purposes, including instance management, cost queries, and IAM role
creation.

------------------------------------------------------------------------

## 🤔 Additional Notes

-   The bot uses emojis to make interactions more intuitive (e.g., ✅
    for successful instance start).
-   It's easily extensible, allowing the addition of new AWS services or
    commands.
-   Future improvements may include AWS Lambda, SQS integration, and
    advanced security monitoring.

------------------------------------------------------------------------

## 🤝 Contribution

Feel free to fork this project and submit pull requests. Make sure you
run tests before submitting.

------------------------------------------------------------------------

## 📄 License

This project is licensed under the MIT License.

Note : we couldn't do the screen record due to time constraints and computer malfuction we request sorry from you but we will provide some snippets of discord bot.
