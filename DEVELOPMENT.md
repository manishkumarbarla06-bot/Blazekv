# BlazeKV Development Guide

## Project Structure

```
blazekv/
├── blazekv.c           # Main source code
├── Makefile            # Build configuration (Linux/macOS)
├── build.sh            # Build script (Linux/macOS)
├── build.bat           # Build script (Windows)
├── README.md           # Project documentation
├── LICENSE             # MIT License
├── .gitignore          # Git ignore rules
├── EXAMPLES.md         # Usage examples
└── DEVELOPMENT.md      # This file
```

## Building

### Windows
```bash
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

Or use Make:
```bash
make build
```

## Development Workflow

1. **Edit Code**: Modify `blazekv.c` as needed
2. **Compile**: Run the appropriate build script
3. **Test**: Run `./blazekv` and test commands
4. **Commit**: Use git to track changes

## Code Structure

- **Header Comments**: Explain file purpose and metadata
- **Function Documentation**: Each function has a docstring
- **Constants**: Configuration values defined at the top
- **Global State**: Database array and counter
- **Core Functions**:
  - `load_db()` - Load from disk
  - `save_db()` - Persist to disk
  - `find_index()` - Search for key
  - `set()` - Store/update key-value
  - `get()` - Retrieve value
  - `del()` - Delete key-value
  - `repl()` - Interactive interface
  - `main()` - Entry point

## Performance Considerations

Current implementation:
- **Time Complexity**: O(n) for get/set/del (linear search)
- **Space Complexity**: O(n) for database storage
- **Suitable for**: Up to 1000 entries

Future improvements:
- Hash table for O(1) operations
- B-tree for sorted iteration
- Network interface for remote access
- Compression for large values

## Testing

Manual testing checklist:
- [ ] Compile without warnings
- [ ] Set and retrieve values
- [ ] Update existing keys
- [ ] Delete keys
- [ ] Retrieve non-existent keys
- [ ] Data persists between sessions
- [ ] Handle boundary cases (empty keys, long values)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Common Issues

### Issue: "No C compiler found"
**Solution**: Install GCC, MSVC, or MinGW depending on your platform

### Issue: Permission denied on build.sh
**Solution**: Run `chmod +x build.sh` first

### Issue: Database corruption
**Solution**: Delete `data.db` and restart to reset the database

## Future Roadmap

- [ ] Hash table implementation
- [ ] Command-line arguments (no REPL mode)
- [ ] Key expiration (TTL)
- [ ] Multiple databases
- [ ] Network interface
- [ ] Statistics/monitoring
- [ ] Transaction support
- [ ] Backup/restore
