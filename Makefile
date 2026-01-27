PREFIX ?= /usr
DESTDIR ?=
PKGNAME = main-keyboard

.PHONY: install uninstall

install:
	# Install Python files
	install -Dm755 main.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/main.py
	install -Dm644 keyboard.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/keyboard.py
	install -Dm644 input_emitter.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/input_emitter.py
	install -Dm644 layouts/__init__.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/layouts/__init__.py
	install -Dm644 layouts/de.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/layouts/de.py
	install -Dm644 layouts/uk.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/layouts/uk.py
	install -Dm644 layouts/us.py $(DESTDIR)$(PREFIX)/share/$(PKGNAME)/layouts/us.py

	# Install launcher script
	install -Dm755 /dev/stdin $(DESTDIR)$(PREFIX)/bin/$(PKGNAME) << 'EOF'
#!/bin/bash
cd $(PREFIX)/share/$(PKGNAME) && python3 main.py "$$@"
EOF

	# Install desktop entry
	install -Dm644 main-keyboard.desktop $(DESTDIR)$(PREFIX)/share/applications/$(PKGNAME).desktop

	@echo ""
	@echo "Installation complete!"
	@echo "Make sure your user has access to /dev/uinput:"
	@echo "  sudo usermod -aG input $$USER"
	@echo "Then log out and back in."
	@echo ""
	@echo "Start with: main-keyboard"

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/$(PKGNAME)
	rm -rf $(DESTDIR)$(PREFIX)/share/$(PKGNAME)
	rm -f $(DESTDIR)$(PREFIX)/share/applications/$(PKGNAME).desktop
	@echo "Uninstalled $(PKGNAME)"
