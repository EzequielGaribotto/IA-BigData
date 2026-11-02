# Notas de WSL

## 2026-10-27: python3.11 se cayó varias veces seguidas

**Qué pasó.** Entre las 14:40 y las 14:47, WSL dejó 10 volcados de memoria (`.dmp`, unos 2 GB cada uno, 12,7 GB en total) en `C:\Users\Eze\AppData\Local\Temp\wsl-crashes`:

- 9 de `/usr/bin/python3.11`: es el Python de `venv_iabd`; `venv_autoeda` usa 3.12.
- 1 del `node` del servidor de VS Code (`~/.vscode-server`).

Los volcados se enviaron a la papelera de Windows el 2026-10-29 para liberar espacio. Si vuelve a pasar, aparecerán de nuevo en esa carpeta.

**Causa probable.** El número al final del nombre del volcado es la señal que mató al proceso:

- `python3.11-…-11.dmp` → señal 11 (SIGSEGV, *segmentation fault*): un fallo dentro de código nativo (C/C++/CUDA de alguna librería, p. ej. PyTorch, TensorFlow o transformers), no un error de Python.
- `node-…-4.dmp` → señal 4 (SIGILL).

**No fue falta de memoria**: cuando WSL se queda sin RAM, el kernel mata el proceso con SIGKILL (9) y no deja volcado. Además, cada proceso ocupaba ~2 GB, lejos del límite por defecto de WSL (50 % de la RAM, ~16 GB de 32 GB; no hay `.wslconfig`).

Ese día se tocaron los notebooks de `M03_ProgramacionDeIA/RA2/T3` (DistilBERT, PyTorch), `RA2/T4` (agentes) y `M_ProyectoIABD/T2` (AutoEDA), así que el fallo vino probablemente de alguno de ellos. Que fueran 4 caídas en 1 minuto (14:40–14:41) sugiere un kernel de Jupyter que se reiniciaba y volvía a fallar en la misma celda.

**Si vuelve a pasar:**

1. Justo después del fallo, en WSL: `dmesg | tail -50` (busca `segfault` o `Out of memory`).
2. Mira qué celda o librería lo provoca (ejecuta las celdas una a una). Los segfaults suelen deberse a versiones incompatibles entre `torch`/`tensorflow`, `numpy` y CUDA: prueba a actualizar o fijar versiones en `venv_iabd`.
3. Solo si `dmesg` muestra `Out of memory`, sube la memoria de WSL creando `C:\Users\Eze\.wslconfig`:

   ```ini
   [wsl2]
   memory=24GB
   swap=8GB
   ```

   y reinicia WSL con `wsl --shutdown`.
4. Borra los `.dmp` de `%LOCALAPPDATA%\Temp\wsl-crashes` cuando ya no los necesites: ocupan mucho.
