CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = blazekv
SOURCE = blazekv.c
DBFILE = data.db

.PHONY: all build run clean help

all: build

build: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)
	@echo "✅ BlazeKV built successfully!"

run: build
	./$(TARGET)

clean:
	rm -f $(TARGET) $(DBFILE)
	@echo "🧹 Cleaned build artifacts"

help:
	@echo "BlazeKV - Ultra-fast Key-Value Store"
	@echo ""
	@echo "Available targets:"
	@echo "  make build   - Build the project"
	@echo "  make run     - Build and run BlazeKV"
	@echo "  make clean   - Remove build artifacts"
	@echo "  make help    - Show this help message"
