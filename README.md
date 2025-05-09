# Stream-Controller VTubeStudio Plugin

This is a plugin for integrating [VTube Studio](https://denchisoft.github.io/VTubeStudio/), using [pyvts](https://github.com/Genteki/pyvts) with the **Stream-Controller** application. It enables live interaction and control of VTube Studio models, expressions, and parameters directly from your streaming setup or external triggers.

## Features

- Connects to VTube Studio using the official WebSocket API.
- Syncs model information and toggles hotkeys or expressions.
- Exposes an interface for Stream-Controller to trigger VTS events.
- Supports real-time updates through an Observer pattern.

## Usage

The plugin will:

- Automatically connect to VTube Studio.
- Provide a synchronous wrapper (`SyncVTSController`) for compatibility with non-async Stream-Controller code.
- Listen for RPC calls and execute corresponding VTS actions.

You can use it to:

- Toggle expressions.
- Change model parameters.
- React to Stream-Controller events.

## License

MIT License. See `LICENSE` for details.
For more information checkout [the docs](https://streamcontroller.github.io/docs/latest/).
