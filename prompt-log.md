# Prompt Log

This file records each assistant interaction in this workspace.

## 2026-03-25

### Interaction
- **Timestamp:** 2026-03-25
- **User request:** Create or append to a `prompt-log.md` file to log all interactions. Confirm that you can write to disk continuously without manual reminders.
- **Assistant action:** Created `prompt-log.md` in the workspace root and wrote the first log entry.
- **Assistant confirmation:** I can write to disk and append to this log automatically on subsequent interactions without needing manual reminders.

### Interaction
- **Timestamp:** 2026-03-25
- **User request:** Create a singleton metaclass suitable to be used for initialising only instance of an object (e.g. a database session)
- **Assistant action:** Added a thread-safe `SingletonMeta` metaclass and a `DBSession` singleton wrapper to `database.py`, plus a `get_session()` helper.

### Interaction
- **Timestamp:** 2026-03-25
- **User request:** What is the correct type interface for a boolean in graphql?
- **Assistant action:** Answered that GraphQL uses the `Boolean` scalar type (e.g. `flag: Boolean` or `flag: Boolean!`).

### Interaction
- **Timestamp:** 2026-03-25
- **User request:** Consider the design.rtf and requirements.rtf file. Whats the best way to handle versions with books? Should we keep track of versions as an integer column on each row in the database, or should we have a separate versions table, or can we just track them as a JSONB column? Consider only the scope at hand.
- **Assistant action:** Recommended using a separate versions/snapshots table for per-work version history; suggested JSONB only for storing field-level diffs if needed.

### Interaction
- **Timestamp:** 2026-03-25
- **User request:** Okay I have finished designing the schema... can you check that it is valid and it meets the design requirements speicifd in design.rtf?
- **Assistant action:** Reviewed `graphql/schema.graphql` against `workings/design.rtf` and `workings/requirements.rtf` and identified GraphQL SDL validity issues (missing types/fields) plus requirement coverage gaps (pagination, single-book detail, version retrieval surface, and activity log querying).

### Interaction
- **Timestamp:** 2026-03-25T15:10:07Z (UTC)
- **User request:** Can you track timestamps in the prompt log going forward too and fix the issues in the schema while preserving its design
- **Assistant action:** Updated the GraphQL SDL to be valid (added `scalar JSON`, defined missing `LogResponse`, and ensured `Book`/`BookVersion` fully satisfy the `Work` interface). Also started recording exact ISO-8601 timestamps for new prompt-log entries.

### Interaction
- **Timestamp:** 2026-03-25T15:11:54Z (UTC)
- **User request:** Why did you duplicat the fields of the Worjk Interface in both book and book version?
- **Assistant action:** Logged this explanation: GraphQL requires interface implementers to define all interface fields, so `BookVersion implements Work` needs the same fields as `Book`. Proposed alternative refactor: split interfaces or remove `implements Work` from `BookVersion` if you don't need it.

### Interaction
- **Timestamp:** 2026-03-25T15:19:23Z (UTC)
- **User request:** Compose the docker container with a postgres database and expose port 3025 and mount to the local volumes for the api.
- **Assistant action:** Updated `docker-compose.yml` to run an `api` service (host `3025:3025`, bind-mount repo to `/home/app`, persist `/home/app/venv`) alongside a `postgres` service, and set API DB env vars to use the `postgres` service name.

### Interaction
- **Timestamp:** 2026-03-25T15:24:04Z (UTC)
- **User request:** Thank you, next can you assist me by creating all the models required from the design.rtf and the requirements.rtf... I have set up the models.py base class so inherit from this and adhere to SqlAlchemy 2.0 model definitions and make sure you type things correctly with Mapped[Type] and also add any foreign keys or indexes that are required and make sure to succintly justify anything.
- **Assistant action:** Implemented SQLAlchemy 2.0 models in `models.py`: `Tenant`, `Book`, `BookVersion`, `ReadingListSubmission`, `ReadingListItem`, `IngestionActivityLog`, and `AsyncJob`, with appropriate foreign keys, indexes, JSONB fields for arrays/diffs, and concise in-code justifications for hashed/dedupe and reading-list identifiers.
