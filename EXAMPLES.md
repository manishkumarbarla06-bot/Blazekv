# BlazeKV Usage Examples

## Basic Operations

### Starting BlazeKV
```bash
$ ./blazekv
🔥 BlazeKV v1.0 — Minimal Key-Value Store Loaded
>
```

### Setting Values
```
> set username "alice"
OK
> set email "alice@example.com"
OK
> set counter "42"
OK
```

### Getting Values
```
> get username
alice
> get email
alice@example.com
> get counter
42
```

### Getting Non-existent Keys
```
> get nonexistent
(null)
```

### Deleting Keys
```
> del counter
OK
> get counter
(null)
```

### Updating Values
```
> set username "bob"
OK
> get username
bob
```

### Exiting
```
> exit
```

## Session Example

```
> set db_version "1.0"
OK
> set last_user "admin"
OK
> get db_version
1.0
> get last_user
admin
> set last_user "guest"
OK
> get last_user
guest
> del db_version
OK
> exit
```

## Notes

- Data persists between sessions (saved to `data.db`)
- All keys and values are stored as strings
- Maximum key length: 256 characters
- Maximum value length: 1024 characters
- Maximum total entries: 1000
