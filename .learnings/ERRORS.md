# Errors Log

This file records command failures, exceptions, and unexpected behavior.

## Format

Each entry should include:
- **ID**: ERR-YYYYMMDD-XXX
- **Logged**: ISO-8601 timestamp
- **Priority**: low | medium | high | critical
- **Status**: pending | in_progress | resolved | wont_fix
- **Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description

### Error
```
Actual error message
```

### Context
- Command attempted
- Input/parameters
- Environment details

### Suggested Fix
If identifiable

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
- See Also: ERR-YYYYMMDD-XXX

---
