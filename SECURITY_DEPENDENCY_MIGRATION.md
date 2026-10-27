# Security dependency migration

This candidate moves to Python 3.11+ for patched Pillow 13, Streamlit and Arrow.
Python 3.10 is no longer supported. Keep the Poetry manifest, `poetry.lock` and
the exported `requirements.txt` together; install from the lock/requirements.

Pillow 9.5.0 → 13.0.0 and Streamlit 1.22.0 → 1.66.1 require a migration, not a
blind patch upgrade. Telegram 20.6 → 22.8 permits the maintained HTTP transport;
the existing async send-message call is preserved. Pydantic remains on the v1
line so `BaseSettings` and the existing models retain their API.

Security floors cover the previously vulnerable HTTP, template, image, Arrow,
protobuf and tooling packages. The candidate lock was compared locally with the
downloaded public OSV PyPI database: no matching advisory versions remained at
the audit date. This does not certify exploit reachability or future safety.

Offline compatibility checks:

```sh
python -m unittest -v test_dependency_compatibility
```

Provide fixture-only `RPC_USER`, `RPC_PASSWORD`, `RPC_HOST` and `RPC_PORT` when
running checks: importing the existing configuration requires those values.
The tests mock RPC, HTTP and Telegram and exercise settings, dataframes, Arrow,
Plotly and the local logo. Do not run the existing integration tests against a
real node as part of this verification. Check the dashboards and actual
deployment Python before release; a full live dashboard/RPC/Telegram test is
still required. No production environment or credential is changed by this PR.

The old requirements were stale transitive pins. Re-export after changing the
manifest using the Poetry export plugin; do not edit only a single pin.
