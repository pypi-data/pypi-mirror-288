![Header](https://raw.githubusercontent.com/george-jensen/record-and-play-pynput/main/READMEHeader.png "Header")

## Description

This project enables the recording of keyboard and mouse inputs, which can be played back with looping functionality using the pynput library. It is designed to facilitate the automation of repetitive computer tasks efficiently, whatever they may be.

## Installation

### Install via PyPi

You can install this package directly from PyPi:

```bash
pip install record-and-play-pynput
```

### Install from GitHub

Alternatively, you can clone the repository and install the dependencies manually:

1. Clone or download this repository:

```bash
git clone https://github.com/george-jensen/record-and-play-pynput.git
```

2. Navigate to the repository directory:

```bash
cd record-and-play-pynput
```

3. Install the required dependencies using Poetry:

```bash
poetry install
```

## Usage

### Recording

1. Run the `record` command, specifying the required `name_of_recording` argument. Example:

```bash
record-and-play record -n <name_of_recording>
```

All keyboard and mouse activity will be recorded.

2. To end the recording:

- Press the `Escape` key to stop the keyboard recording.
- Hold the right mouse button for more than 2 seconds without moving the mouse, then release to stop the mouse recording.

### Playback

1. Run the `play` command, specifying the `name_of_recording` and the `number_of_requests` arguments. Example:

```bash
record-and-play play -n <name_of_recording> -p <number_of_repeats>
```

2. To stop the playback early, trigger a `KeyboardInterrupt` by pressing `Ctrl+C` in the terminal window.

## Notes

Scrolling functionality is supported, however it is not completely precise. So it is recommended to drag scrollbars when available. If you find you need to scroll to the top or bottom of pages then try and over-compensate when recording before continuing.

## Compatablitity

At the moment this is Mac compatible - I haven't been able to find a Mac compatible tool that does a similar job and that is one of the reasons for this repository's creation.

It has recently been brought to my attention that there are issues with Windows compatability. I will try and address these soon.

<h2>Authors</h2>
George Jensen

<h2>Support!</h2>
If you found this tool useful please give this repo a star!

Please also feel free to create an issue to give feedback on any bugs, or ask for improvements! I'm always keen to keep things up to date and useful so any and all feedback is welcome!
