# Cloudflare Worker asset

`@altertable/data-app-worker` resolves to a precompiled, self-contained ESM Worker
script. Upload this one file as the deployment's main module. It includes the
bootstrap and HTML; no bundling, HTML generation,
runtime imports, or asset fetches are needed in the hosting backend.

This export is a script asset, not a Node.js or Bun API. Pin an exact package
version and commit the lockfile. Resolve and read the installed asset, then pass
its contents to your deployment tooling:

```js
import { readFile } from 'node:fs/promises';

const workerScript = await readFile(
  new URL(import.meta.resolve('@altertable/data-app-worker')),
  'utf8'
);
// Upload workerScript as worker.js, with main_module = "worker.js".
```

The hosting backend retains ownership of domains, routes, deployment settings,
and these string bindings:

| Binding          | Meaning                                                                    | Example                                                 |
| ---------------- | -------------------------------------------------------------------------- | ------------------------------------------------------- |
| `DOMAIN_NAME`    | Runtime domain without scheme, port, or trailing dot                       | `apps.example.net`                                      |
| `PARENT_ORIGINS` | Space-separated trusted HTTP(S) origins; first exact origin is the default | `https://app.example.com https://*.preview.example.com` |

Serve `/` on unique hyphenated lowercase preview labels under `DOMAIN_NAME`,
such as `report-123.apps.example.net`. Other hosts and paths return 404.

`__altertable_parent` selects an exact trusted origin from `PARENT_ORIGINS`; it
cannot add trust. Wildcards allow one HTTPS subdomain label without a port.
Exact entries must be bare HTTP(S) origins. Keep an exact origin first for the
default parent.

The Worker sets CSP and trusted frame ancestors. Data queries use the
[host's authorized SQL route](embed.md#sql-query-route); the Worker does not
execute queries.

For file-based deployment tools such as Terraform, copy the resolved asset
unchanged. Upgrade the host package and Worker together for protocol changes.
Custom bootstrap hosts use [startDataAppBootstrap()](embed.md#trusted-bootstrap).
