---
name: drawio-architecture
description: >
  Generate a draw.io XML file with AWS architecture icons from Terraform code.
  Use when the user asks to create an architecture diagram, draw.io diagram,
  or infrastructure visualization from a Terraform project.
---

# draw.io Architecture Diagram from Terraform

Generate a `.drawio` file with AWS architecture icons by reading the Terraform code in the project.

## Process

1. **Read the Terraform files** - scan `*.tf` files to identify all AWS resources, data sources, and their relationships (security group references, subnet associations, depends_on, etc.)
2. **Identify logical services** - group resources into the services that matter visually: EC2, ALB, S3, Route 53, ACM, SSM, VPC, etc. Skip internal resources that don't add visual value (IAM policies, policy attachments, archive files).
3. **Map connections** - follow references between resources to determine arrows: DNS -> ALB, ACM -> ALB, ALB -> EC2, EC2 <-> S3, etc. Bidirectional arrows for backup/restore patterns.
4. **Generate the draw.io XML** - write the `.drawio` file following the layout principles below.

## Layout Principles

- **Compact** - VPC group is small and tight, no wasted space
- **Icons in line, equidistant** - arrange on a regular grid, not scattered
- **Straight arrows by default** - use `edgeStyle=orthogonalEdgeStyle` only when a straight line would overlap another element
- **Pragmatic workarounds** - if an arrow covers a label, add `&amp;nbsp;` before the label text; if a straight arrow crosses a group border badly, switch to orthogonal for that edge only

## AWS Icon Styles

Use the `mxgraph.aws4` stencil library. Color by AWS service category:

| Category | fillColor | Services |
|----------|-----------|----------|
| Compute | `#ED7100` | EC2 |
| Networking | `#8C4FFF` | ALB, Route 53, VPC |
| Security | `#DD344C` | ACM, IAM, SSM |
| Storage | `#3F8624` | S3 |

### Shape references

| Service | Style |
|---------|-------|
| EC2 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2` |
| ALB | `shape=mxgraph.aws4.application_load_balancer` |
| Route 53 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.route_53` |
| ACM | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.certificate_manager_3` |
| S3 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3` |
| IAM/SSM | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.identity_and_access_management` |
| VPC (group) | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc` |

### Common icon style template

```
outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=none;fillColor={COLOR};labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;{SHAPE}
```

### VPC group style template

```
points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0
```

## XML Structure

- `id="0"` and `id="1"` (with `parent="0"`) are mandatory root cells
- Elements inside a VPC group: set `parent="vpc_id"`, coordinates are relative to the group
- Elements outside VPC: set `parent="1"`
- Edges between elements in the same group: set `parent` to that group
- Edges between elements in different groups: set `parent="1"`
- Icon size: 60x60
- Labels: use `&lt;br&gt;` for line breaks in `value` attribute

## Edge styles

- **Default (straight):** `strokeColor=#232F3E;`
- **Orthogonal (when needed):** `edgeStyle=orthogonalEdgeStyle;strokeColor=#232F3E;`
- **Bidirectional:** add `startArrow=classic;endArrow=classic;`
- **Dashed (optional access):** add `dashed=1;`

## Output

Write the file to `images/architecture.drawio` in the project root. Tell the user to open it in draw.io to verify the layout and export as PNG.

## Language

All labels in the diagram must be in English, regardless of the language used in the conversation.
