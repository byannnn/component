# component
Test repo for component implementation; a simple, re-usable, connect-able component that interacts with other components like itself via sockets.

Features:
- Asynchronous operations
- `pynng` brokerless socket communication
- Proper process titles

Good for quick prototyping of components, just subclass `Component` and go.

---

TODO:
* pytest
  * Test start/stop functionality
* Full setup script + demo
