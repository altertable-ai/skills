# Author a local data app

Use the local scaffold supplied by your authoring workflow. Its README covers
setup and its AGENTS.md identifies app-owned files.
Replace the connectivity screen or fixture examples with the content specified by
the app brief, using the [shared SDK patterns](app-authoring.md). Local execution
does not require a particular content structure or presentation story.

| Task                         | Documentation                            |
| ---------------------------- | ---------------------------------------- |
| Customize local serving      | [Bun server](server-bun.md)              |
| Authorize hosted viewers     | [Server](server.md)                      |
| Customize the browser client | [HTTP client](client.md#http-operations) |

You can also [convert the local app to a hosted data app](hosted-apps.md#convert-a-local-data-app).

## Preview the use-case starters

From the SDK repository, run `bun run dev:gallery` with Docker available. It starts
and seeds the Altertable mock with fictional sample data.

| Starter | Hosted preview                                    | Local preview            |
| ------- | ------------------------------------------------- | ------------------------ |
| Metric  | <http://127.0.0.1:27418/starter-metric-data-app>  | <http://127.0.0.1:27421> |
| Finding | <http://127.0.0.1:27418/starter-finding-data-app> | <http://127.0.0.1:27422> |

Copied starters use the normal query connection. Replace their example queries
with verified sources in the target lakehouse; the mock and seed belong only to
local development. Never create demo objects in a user's lakehouse.
