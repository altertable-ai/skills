---
name: integrating-external
compatibility: Requires Altertable MCP server
description: Connects to external MCP servers and services for extended capabilities. Use when integrating with Amplitude, Omni, Slack, or other external tools, or when configuring notifications and external data sources.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Integrating External

## Quick Start

When a user asks about external integrations:
1. Check which integrations are available via the Altertable MCP server
2. Identify the integration type the user needs (data source, notification, or MCP server)
3. Help the user configure the integration
4. Verify the connection is working

## When to Use This Skill

- User wants to connect an external data source (Amplitude, Omni, etc.)
- User wants to send notifications to Slack or other channels
- User wants to set up or troubleshoot an MCP server connection
- User wants to configure webhooks for alerts or data sync

## Core Workflow

### Step 1: Identify the Integration Type

Ask what the user is trying to accomplish, then map to the right integration:

| Goal | Integration Type |
|------|-----------------|
| Query product analytics events, cohorts, funnels | Amplitude MCP |
| Query metrics, dashboards, reports | Omni MCP |
| Send alerts or share discoveries | Slack notifications |
| Push data to external systems | Webhooks |
| Pull data from external APIs | Data connectors |

### Step 2: Check Existing Configuration

Before setting up a new integration:
- List currently connected MCP servers and their status (each MCP server has a slug, OAuth state, and connection status)
- Check if the requested integration is already configured
- Verify credentials and permissions are in place

### Step 3: Configure the Integration

Follow the integration-specific procedure below.

### Step 4: Verify the Connection

After configuration:
- Run a test query or send a test notification
- Confirm the response is valid and data flows correctly
- Report the result to the user

## Amplitude Integration

To connect or use Amplitude:
1. Verify the Amplitude MCP server is registered and reachable
2. Confirm the API key is configured (stored as an environment variable, never hardcoded)
3. Use available Amplitude tools to query events, cohorts, funnels, or retention data
4. Return results to the user or feed them into insight creation

Available operations: query events, get cohorts, run funnel analysis, get retention data, export reports.

## Omni Integration

To connect or use Omni:
1. Verify the Omni MCP server is registered and reachable
2. Confirm credentials are configured
3. Use available Omni tools to query metrics, list dashboards, run reports, or explore dimensions
4. Return results to the user or feed them into insight creation

Available operations: query metrics, list dashboards, get reports, explore data.

## Slack Integration

Slack connects via OAuth and delivers notifications through an incoming webhook URL.

To set up or use Slack notifications:
1. Check if a Slack connection is already configured for the organization
2. If not, guide the user through connecting their Slack workspace via the Altertable settings (OAuth flow)
3. Help the user choose the target channel and notification types:
   - Discovery alerts for new findings
   - Watcher notifications for automated monitoring
   - Channel posts for team updates
4. Send a test notification to confirm delivery

To disconnect Slack, use the disconnect tool. This removes the OAuth identity and stops all Slack notifications.

## Webhook Configuration

To set up webhooks:
1. Determine direction: incoming (receive data) or outgoing (send alerts/data)
2. For outgoing webhooks: configure the target URL, authentication, and payload format
3. For incoming webhooks: provide the webhook endpoint URL and expected payload schema
4. Test the webhook with a sample payload and verify the response

## Data Connectors

To connect an external API as a data source:
1. Get the API base URL and authentication details from the user
2. Configure the connection with appropriate auth (API key, bearer token, or OAuth)
3. Define the endpoints to query and their expected response format
4. Test the connection with a sample request
5. Never store credentials in plain text -- always use environment variables

## Common Pitfalls

- Attempting to configure an integration that is already active (check existing connections first)
- Hardcoding credentials instead of using environment variables
- Not testing the connection after setup -- always verify with a live request
- Sending notifications to the wrong Slack channel without confirming with the user
- Ignoring rate limits on external APIs, causing requests to fail silently
- Creating duplicate MCP server registrations for the same service

## Reference Files

- [MCP servers](references/mcp-servers.md)
- [Slack notifications](references/slack-notifications.md)
