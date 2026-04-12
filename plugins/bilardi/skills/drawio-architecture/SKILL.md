---
name: drawio-architecture
description: >
  Generate a draw.io XML file with architecture icons by analyzing the project code.
  Use when the user asks to create an architecture diagram, draw.io diagram,
  or infrastructure visualization from any project.
---

# draw.io Architecture Diagram

Generate a `.drawio` file with architecture icons by analyzing the project code, infrastructure files, and existing diagrams.

## Process

1. **Analyze the project** - scan ALL available sources to understand the architecture:
   - Source code: server frameworks (FastAPI, Express, Django) for endpoints and protocols; SDK imports (`boto3`, `@aws-sdk/*`) for managed services; client code for connection patterns (WebSocket, HTTP, gRPC)
   - Infrastructure: `*.tf` files for AWS resources and relationships; `docker-compose.yaml` for services and networking; `Dockerfile` for exposed ports
   - Existing diagrams: mermaid blocks in README.md or docs
   - Architecture docs: POST.md, design docs, specs
2. **Identify components** - determine what matters visually. Assign each component a role:
   - **Managed service**: cloud services called via SDK (Transcribe, S3, DynamoDB)
   - **Server**: self-managed servers and APIs (FastAPI, Express, nginx)
   - **Client**: user-facing applications (browser, mobile, CLI tool)
   - **Physical device**: hardware (microphone, monitor, mixer, printer)
   - Skip internal details that don't add visual value (IAM policies, policy attachments, archive files)
3. **Map data flow** - follow the code to determine arrows and protocols:
   - API endpoints: who calls them, what they return
   - SDK calls: what external services are involved, request/response pattern
   - Communication channels: WebSocket, event streams, queues, physical connections
   - Bidirectional flows: backup/restore, request/response on same channel
4. **Group by environment** - determine natural groupings:
   - Self-managed (runs on your infra: servers, clients, devices)
   - Managed services per provider (AWS, GCP, Azure)
   - Physical/on-premise
   - Network boundaries (VPC, subnets) when relevant
5. **Check mermaid consistency** - if a mermaid diagram exists in the project, compare it with what the code analysis found. Flag any inconsistencies to the user before generating the drawio: missing components, wrong connections, outdated grouping.
6. **Generate the draw.io XML** - write the `.drawio` file following the layout principles and theme below.

## Layout Principles

- **Compact** - groups are small and tight, no wasted space
- **Icons in line, equidistant** - arrange on a regular grid, not scattered
- **Straight arrows by default** - use `edgeStyle=orthogonalEdgeStyle` only when a straight line would overlap another element
- **Pragmatic workarounds** - if an arrow covers a label, add `&amp;nbsp;` before the label text; if a straight arrow crosses a group border badly, switch to orthogonal for that edge only

## Theme

Use the `mxgraph.aws4` stencil library as the primary icon source. For icon names not listed here, search the draw.io stencil browser or the AWS Architecture Icons page.

### Color palette by category

| Category | fillColor | When to use |
|----------|-----------|-------------|
| Compute | `#ED7100` | servers, containers, Lambda, EC2 |
| Networking | `#8C4FFF` | ALB, Route 53, VPC, API Gateway |
| Security | `#DD344C` | ACM, IAM, SSM, Cognito |
| Storage | `#3F8624` | S3, DynamoDB, RDS, EBS |
| ML/AI | `#01A88D` | Transcribe, SageMaker, Comprehend, Rekognition |
| Generic/Client | `#232F3E` | PCs, browsers, user devices, CLI tools |
| Physical device | `#dae8fc` fill + `#6c8ebf` stroke | microphones, monitors, mixers, printers |

### Style templates by role

**Managed service** (AWS/cloud icon with category color):

```
outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=none;fillColor={CATEGORY_COLOR};labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service_name}
```

**Server/Client** (generic icon with category color):

```
outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=none;fillColor={CATEGORY_COLOR};labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.{icon_name}
```

Common icon names: `client` (laptop), `traditional_server` (server rack), `mobile_client` (phone), `users` (people).

**Physical device** (simple shape):

```
rounded=1;whiteSpace=wrap;html=1;fillColor={LIGHT_COLOR};strokeColor={DARK_COLOR};fontSize=11;fontStyle=0;verticalAlign=middle;align=center;
```

### Group styles

**AWS group** (cloud, VPC, region):

```
points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=14;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon={GROUP_ICON};strokeColor={STROKE_COLOR};fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0
```

| Type | grIcon | strokeColor |
|------|--------|-------------|
| AWS Cloud | `mxgraph.aws4.group_aws_cloud` | `#232F3E` |
| VPC | `mxgraph.aws4.group_vpc` | `#8C4FFF` |
| Region | `mxgraph.aws4.group_region` | `#00A4A6` |

**Generic group** (on-premise, self-managed, physical):

```
rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#232F3E;dashed=1;verticalAlign=top;align=left;spacingLeft=10;fontSize=14;fontStyle=1;fontColor=#232F3E;container=1;collapsible=0;recursiveResize=0;
```

## XML Structure

- `id="0"` and `id="1"` (with `parent="0"`) are mandatory root cells
- Elements inside a group: set `parent` to the group id; coordinates are relative to the group
- Elements outside any group: set `parent="1"`
- Edges between elements in the same group: set `parent` to that group
- Edges between elements in different groups: set `parent="1"`
- Icon size: 60x60
- Labels: use `&lt;br&gt;` for line breaks in `value` attribute

## Edge styles

- **Default (straight):** `strokeColor=#232F3E;fontSize=9;fontColor=#232F3E;labelBackgroundColor=#FFFFFF;`
- **Orthogonal (when needed):** add `edgeStyle=orthogonalEdgeStyle;`
- **Bidirectional:** add `startArrow=classic;endArrow=classic;`
- **Dashed (optional access):** add `dashed=1;`

## Output

Write the file to `images/architecture.drawio` in the project root. Tell the user to open it in draw.io to verify the layout and export as PNG.

## Language

All labels in the diagram must be in English, regardless of the language used in the conversation.
