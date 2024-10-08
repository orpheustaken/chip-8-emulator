<div align="center">
  <h1>CHIP-8 Emulator</h1>
  <p>CHIP-8 interpreter written in Python</p>
</div>

[![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/ambv/black)

There certainly are improvements to be made here, but I am satisfied with the current state of this project and I was able to learn a lot as this was my first emulator. For now I'll just leave this as is.

Usage
```
python main.py <rom_img_path>
```

Note: Install the `requirements.txt` dependencies first. I've used [Pyglet](https://github.com/pyglet/pyglet) to abstract all the OpenGL boilerplate.

<div align="center">
  <img src=https://github.com/user-attachments/assets/a9dd9f16-bbf1-40f4-9fcd-b544741637f1>
  <img src=https://github.com/user-attachments/assets/cf2323dc-f714-4ff8-97d4-6f22083e7970>
  <img src=https://github.com/user-attachments/assets/49296de5-c884-4eaa-882b-f7b045080a99>
</div>

Documentation
- [Spec](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)
- [Walkthrough](https://omokute.blogspot.com/2012/06/emulation-basics-write-your-own-chip-8.html)
- [ROMs](https://github.com/kripod/chip8-roms)
