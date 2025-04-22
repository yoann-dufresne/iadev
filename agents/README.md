# Agents

This directory contains the description of the agents that are used by the framework.
If you are looking for agents created for your project, please look inside of the output directory of your project.

## yaml format

The agents are defined as follow

```yaml
    name: Agent name
    description: The prompt for the agent that will be send as a "system" role.
    tools: [The list of the tools that the agent can use (Optional)]
```