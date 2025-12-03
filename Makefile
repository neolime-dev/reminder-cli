PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	@echo "Installing reminder..."
	install -d $(BINDIR)
	install -m 755 reminder.py $(BINDIR)/reminder
	@echo "Done! You can now run 'reminder'."

uninstall:
	@echo "Removing reminder..."
	rm -f $(BINDIR)/reminder
	@echo "Done."
