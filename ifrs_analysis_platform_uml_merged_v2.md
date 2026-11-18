# IFRS Analysis Platform: Complete UML Specification (v2)

This document consolidates the core domain model (v1) with the updated access control, billing, and entitlement architecture (v2). It supersedes `Membership` and basic `Subscription` models from v1 while preserving the data versioning, IFRS analysis, and posting workflows.

---

## 1. Domain Class Diagrams

To maintain readability, the domain is split into two connected views: **Access & Billing** (v2) and **Data Versioning, IFRS Analysis & Posting** (v1 core).

### 1.1 Access Control, Collaboration & Billing

Being in a workspace and having access to a project are separate grants. `WorkspaceMember` grants visibility into the workspace, while `ProjectMember` grants access to specific projects unless `access_scope` is set to `all_projects`. Subscriptions live on the workspace owner; invitees ride on the owner's subscription.

```mermaid
classDiagram
direction LR
class User {
  +uuid id
  +string email
  +bool verified
}
class Workspace {
  +uuid id
  +string name
  +uuid owner_user_id
  +uuid subscription_id
}
class WorkspaceMember {
  +uuid user_id
  +uuid workspace_id
  +enum access_scope
  +string role
  +datetime joined_at
}
class Project {
  +uuid id
  +uuid workspace_id
  +string name
  +enum ifrs_standard
  +bool archived
}
class ProjectMember {
  +uuid user_id
  +uuid project_id
  +uuid granted_by
  +datetime granted_at
}
class Invitation {
  +uuid id
  +uuid workspace_id
  +string email
  +string token_hash
  +enum access_scope
  +enum status
  +datetime expires_at
  +uuid invited_by
  +uuid accepted_by
}
class InvitationProject {
  +uuid invitation_id
  +uuid project_id
}
class Plan {
  +uuid id
  +string name
  +enum type
  +int duration_days
  +decimal price
  +string currency
  +json limits
}
class Subscription {
  +uuid id
  +uuid owner_user_id
  +uuid plan_id
  +enum status
  +datetime started_at
  +datetime period_start
  +datetime period_end
  +datetime grace_until
  +datetime canceled_at
}
class Invoice {
  +uuid id
  +uuid subscription_id
  +string number
  +decimal amount
  +string currency
  +enum status
  +date issued_on
  +date due_on
}
class InvoiceLine {
  +uuid invoice_id
  +string description
  +decimal quantity
  +decimal unit_price
}
class Payment {
  +uuid id
  +uuid invoice_id
  +decimal amount
  +enum status
  +string method
  +string provider_ref
  +string failure_reason
  +datetime attempted_at
}
class UsageEvent {
  +uuid id
  +uuid subscription_id
  +uuid user_id
  +string metric
  +decimal quantity
  +datetime at
}
class AuditEvent {
  +uuid id
  +string action
  +string entity_type
  +uuid entity_id
  +datetime at
}

User "1" --> "*" WorkspaceMember
Workspace "1" --> "*" WorkspaceMember
Workspace "1" --> "*" Project
User "1" --> "*" ProjectMember
Project "1" --> "*" ProjectMember
Workspace "1" --> "*" Invitation
Invitation "1" --> "*" InvitationProject
InvitationProject "*" --> "1" Project

Plan "1" --> "*" Subscription
Subscription "1" --> "*" Workspace
Subscription "1" --> "*" Invoice
Invoice "1" --> "*" InvoiceLine
Invoice "1" --> "1..*" Payment
Subscription "1" --> "*" UsageEvent
```

#### Access Scope & Invariants

| `access_scope` | Meaning |
| --- | --- |
| `all_projects` | Sees every project in the workspace, including ones created later. No `ProjectMember` rows needed. |
| `selected` | Sees only projects with a `ProjectMember` row. A workspace with zero granted projects still lists, but shows empty. |

* **Invariants:** A `ProjectMember` row requires a `WorkspaceMember` row for the same workspace. Removing a `WorkspaceMember` removes their `ProjectMember` rows. Accepting an invitation copies `InvitationProject` rows into `ProjectMember` rows when `access_scope` is `selected`.

#### Plan Types & Trials

| `Plan.type` | Behavior & Constraints |
| --- | --- |
| `trial` | `duration_days = 14`, `price = 0`, no `Invoice` or `Payment` needed. One per user, enforced by a unique check on `owner_user_id`. |
| `demo` | Fixed sample data and tight limits (e.g., 1 workspace, 0 invitees, no posting). |
| `paid` | Monthly or annual billing; enforces limits such as `max_invitees`, `storage_mb`, and `runs_per_month`. |

* **Trial Upgrades:** Trials end by expiry, not by invoice. The same `Subscription` row moves to a paid `Plan` upon upgrade so workspaces keep pointing at the same subscription ID.

---

### 1.2 Data Versioning, IFRS Analysis & Posting

```mermaid
classDiagram
direction TB
class Workspace {
  +uuid id
  +string name
}
class Project {
  +uuid id
  +uuid workspace_id
  +string name
  +enum ifrs_standard
  +bool archived
}
class ReportingPeriod {
  +uuid id
  +date start
  +date end
  +enum status
}
class Dataset {
  +uuid id
  +string name
}
class DatasetVersion {
  +uuid id
  +string label
  +enum kind
  +uuid parent_version_id
  +datetime created_at
}
class Blob {
  +string sha256
  +long size
  +string storage_path
}
class ProjectDataset {
  +uuid project_id
  +uuid dataset_version_id
  +string role_in_analysis
}
class AssumptionSet {
  +uuid id
  +string name
  +json values
}
class Algorithm {
  +string code
  +string version
  +enum ifrs_standard
}
class AnalysisRun {
  +uuid id
  +json parameters
  +enum status
  +uuid triggered_by
  +datetime started_at
  +datetime finished_at
}
class ResultSet {
  +uuid id
  +string checksum
  +bool immutable
}
class ResultLine {
  +string metric
  +decimal amount
  +string currency
  +json dimensions
}
class PostingBatch {
  +uuid id
  +enum status
  +uuid posted_by
  +datetime posted_at
}
class JournalLine {
  +string account
  +decimal debit
  +decimal credit
}

Workspace "1" --> "*" Project
Workspace "1" --> "*" Dataset
Project "1" --> "*" ReportingPeriod
Project "1" --> "*" ProjectDataset
Project "1" --> "*" AnalysisRun
Dataset "1" --> "*" DatasetVersion
DatasetVersion "*" --> "1" Blob
DatasetVersion "0..1" <-- "*" DatasetVersion : parent
ProjectDataset "*" --> "1" DatasetVersion
AnalysisRun "*" --> "1" Algorithm
AnalysisRun "*" --> "1" ReportingPeriod
AnalysisRun "*" --> "0..1" AssumptionSet
AnalysisRun "*" --> "1..*" DatasetVersion : inputs
AnalysisRun "1" --> "0..1" ResultSet
ResultSet "1" --> "*" ResultLine
ResultSet "1" --> "*" PostingBatch
PostingBatch "1" --> "*" JournalLine
```

#### Key IFRS Domain Concepts
* **Algorithm:** Treated as data rather than code identity (`ifrs_standard`, `code`, `version`), ensuring every result explicitly records the logic that produced it.
* **AssumptionSet:** Stores discount rates, macro scenarios, and parameters separately from datasets so assumptions can vary without cloning underlying files.
* **ReportingPeriod:** Groups and locks runs and postings per accounting period.
* **PostingBatch:** Separates analytical output (`ResultSet`) from the accounting decision to book entries. Posted batches are immutable; corrections require reversal batches.

---

## 2. State Lifecycles

### 2.1 Subscription & Entitlement States

```mermaid
stateDiagram-v2
[*] --> Trialing: sign up
Trialing --> Active: first payment succeeds
Trialing --> Expired: 14 days pass
Active --> PastDue: payment fails
PastDue --> Active: payment recovered
PastDue --> Expired: grace ends
Active --> Canceled: user cancels
Canceled --> Expired: period_end reached
Expired --> Active: user pays
Expired --> Archived: retention window ends
```

| Entitlement | Subscription State | Allowed Actions |
| --- | --- | --- |
| `full` | `Trialing`, `Active` | Everything within plan limits. |
| `grace` | `PastDue` (~7 days) | Everything within plan limits, accompanied by a payment warning banner. |
| `read_only` | `Expired`, `Canceled` | View projects, results, and history; download or export. No uploads, runs, postings, or invites. |
| `archived` | Post-retention (e.g., 90 days) | Data moved to cold storage; restorable upon payment or support request. |

### 2.2 Analysis Run Lifecycle

```mermaid
stateDiagram-v2
[*] --> Queued
Queued --> Running
Running --> Complete
Running --> Failed
Complete --> Posted: PostingBatch created
Complete --> Superseded: newer run on same period
Posted --> Reversed: reversal batch
Failed --> [*]
Posted --> [*]
Superseded --> [*]
Reversed --> [*]
```

---

## 3. Data Versioning Tree ("Floating vs. No Floating" Case)

Dataset versions form a directed tree. Each `AnalysisRun` pins the exact `DatasetVersion` IDs it consumes so results always trace back to an immutable branch.

```mermaid
flowchart TD
D["Dataset: June loans"] --> V1["v1 uploaded: june_2023_loans.xls"]
V1 --> V2["v2 derived: floating rates"]
V1 --> V3["v3 derived: no floating rates"]
V2 --> V4["v4 derived: floating, corrected FX"]
V2 -. pinned by .-> R1["Run 1: IFRS 9 ECL"]
V3 -. pinned by .-> R2["Run 2: IFRS 9 ECL"]
V4 -. pinned by .-> R3["Run 3: IFRS 9 ECL"]
R1 --> RS1["ResultSet 1"]
R2 --> RS2["ResultSet 2"]
R3 --> RS3["ResultSet 3"]
```

---

## 4. Authorization & Request Guard Flow

Every project-scoped API request passes through workspace membership, project scope, subscription entitlement, and plan limit checks before execution.

```mermaid
flowchart TD
A["Request: user U, action X, project P"] --> B{"U is WorkspaceMember of P's workspace?"}
B -- no --> Z1["Deny"]
B -- yes --> C{"scope = all_projects, or ProjectMember row for P?"}
C -- no --> Z1
C -- yes --> D["Load workspace subscription"]
D --> E{"X is a read or export?"}
E -- yes --> OK["Allow while not archived"]
E -- no --> F{"Entitlement full or grace?"}
F -- no --> Z2["Deny: read only, upgrade prompt"]
F -- yes --> G{"Within plan limits?"}
G -- no --> Z3["Deny: limit reached"]
G -- yes --> OK2["Allow, write UsageEvent and AuditEvent"]
```

---

## 5. Sequence Diagrams

### 5.1 Login & Session Loading

Login does not gate on the user's personal subscription. Each workspace is evaluated against the subscription attached to that workspace, allowing invitees without their own paid plan to collaborate seamlessly.

```mermaid
sequenceDiagram
actor U as User
participant API
participant DB
U->>API: Login (email, password)
API->>DB: Verify credentials
API->>DB: Load WorkspaceMember rows for user
loop each workspace
  API->>DB: Load workspace subscription and plan
  API->>API: Compute entitlement (full, grace, read_only, archived)
  API->>DB: Load projects (all, or via ProjectMember)
end
API-->>U: Session + workspaces with entitlement + project lists
Note over U,API: Own subscription status is returned too, for the billing banner
```

### 5.2 Invitation with Project Grants

```mermaid
sequenceDiagram
actor Owner
actor Invitee
participant API
participant DB
participant Mail as Email
Owner->>API: Invite email, scope, optional project list
API->>DB: Check max_invitees on owner's plan
API->>DB: Create Invitation + InvitationProject rows
API->>Mail: Send link with raw token
Mail-->>Invitee: Invite link
Invitee->>API: Open link
alt email already registered
  API->>DB: Require login as that email
else new user
  API->>DB: Register with email locked as username
end
API->>DB: Create WorkspaceMember with access_scope
opt scope is selected
  API->>DB: Copy InvitationProject to ProjectMember
end
API->>DB: Invitation status = accepted, write AuditEvent
```

### 5.3 Upload, Version, Analyse & Post

```mermaid
sequenceDiagram
actor U as User
participant API
participant Store as Blob store
participant DB
participant Engine as Analysis engine
U->>API: Upload june_2023_loans.xls
API->>Store: Put bytes (by sha256)
API->>DB: Dataset + DatasetVersion v1 (kind=upload)
API->>DB: AuditEvent(upload)
U->>API: Create derived version (floating rates)
API->>DB: DatasetVersion v2 (parent=v1, kind=derived)
U->>API: Run IFRS 9 ECL on v2 with AssumptionSet
API->>DB: Check entitlement & plan limits, write UsageEvent
API->>DB: AnalysisRun(status=queued, pinned inputs)
API->>Engine: Execute(run_id)
Engine->>Store: Read blob for v2
Engine->>DB: ResultSet + ResultLines (immutable)
Engine->>DB: AnalysisRun status=complete
U->>API: Post results
API->>DB: PostingBatch + JournalLines
API->>DB: AuditEvent(post)
```