"""Partition drill tests for Forge ecosystem connectivity contracts.

These tests simulate network partitions and service failures to verify
that all Forge services behave correctly under degraded conditions:
- Fail-closed when authority is unavailable
- Named degraded modes when non-critical dependencies are down
- Proper error propagation and observability
"""
