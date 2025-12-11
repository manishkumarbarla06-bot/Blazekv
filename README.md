# 🔥 BlazeKV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue.svg)](https://github.com/sponsors/manishkumarbarla06-bot) [![Patreon](https://img.shields.io/badge/Patreon-Support-orange.svg)](https://www.patreon.com/yourname)

An ultra-fast, minimal key-value store written in C. BlazeKV is designed for simplicity, speed, and ease of use.

## Features

- ⚡ **Fast**: Optimized for performance with minimal overhead
- 💾 **Persistent**: Data is automatically saved to disk
- 🎯 **Simple**: Intuitive command-line interface
- 🔧 **Lightweight**: Written in pure C with no external dependencies
- 📦 **Easy to Build**: Single command compilation with Makefile

## Quick Start

### Build
```bash
make
```

### Run
```bash
./blazekv
```

### Usage

BlazeKV provides a simple REPL (Read-Eval-Print Loop) interface:

```
> set mykey "Hello, World!"
OK
> get mykey
Hello, World!
> del mykey
OK
> exit
```

## Commands

- **SET key value**: Store a key-value pair
- **GET key**: Retrieve the value for a key
- **DEL key**: Delete a key-value pair
- **EXIT**: Exit the REPL

## Data Persistence

All data is automatically saved to `data.db`. The database is loaded on startup and persisted after each operation.

## Specifications

- Maximum key size: 256 bytes
- Maximum value size: 1024 bytes
- Maximum entries: 1000

## Building from Source

### Requirements
- GCC compiler
- Make (optional, you can compile directly)

### Compile
```bash
make
```

Or directly:
```bash
gcc blazekv.c -o blazekv
```

## Performance

BlazeKV uses linear search for key lookups, making it suitable for small to medium datasets (up to 1000 entries). For larger datasets, consider a hash table implementation.

## Roadmap

- [ ] Hash table implementation for O(1) lookups
- [ ] Batch operations support
- [ ] Network/TCP interface
- [ ] Expiration keys (TTL)
- [ ] Multiple databases

## License

MIT License - See LICENSE file for details

## Author

BlazeKV Contributors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ in C
