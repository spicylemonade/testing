# Experimental Results

## Baseline Performance (DDA and Bresenham)

| Algorithm | Grid Size | Rays | Distribution | Throughput (rays/s) | Avg Voxels/Ray |
|-----------|-----------|------|-------------|--------------------|--------------|
| dda | 32^3 | 1000 | uniform | 17836 | 20.4 |
| dda | 32^3 | 10000 | uniform | 17892 | 20.6 |
| dda | 32^3 | 1000 | coherent | 11020 | 47.4 |
| dda | 32^3 | 10000 | coherent | 10974 | 47.7 |
| dda | 32^3 | 1000 | axis_aligned | 14183 | 32.0 |
| dda | 32^3 | 10000 | axis_aligned | 14177 | 32.0 |
| dda | 64^3 | 1000 | uniform | 12011 | 41.8 |
| dda | 64^3 | 10000 | uniform | 12002 | 42.3 |
| dda | 64^3 | 1000 | coherent | 6526 | 95.0 |
| dda | 64^3 | 10000 | coherent | 6585 | 95.5 |
| dda | 64^3 | 1000 | axis_aligned | 9109 | 64.0 |
| dda | 64^3 | 10000 | axis_aligned | 9083 | 64.0 |
| dda | 128^3 | 1000 | uniform | 7330 | 84.8 |
| dda | 128^3 | 10000 | uniform | 7274 | 85.5 |
| dda | 128^3 | 1000 | coherent | 3707 | 190.0 |
| dda | 128^3 | 10000 | coherent | 3687 | 191.0 |
| dda | 128^3 | 1000 | axis_aligned | 5302 | 128.0 |
| dda | 128^3 | 10000 | axis_aligned | 5286 | 128.0 |
| bresenham | 32^3 | 1000 | uniform | 21425 | 11.7 |
| bresenham | 32^3 | 10000 | uniform | 21319 | 11.9 |
| bresenham | 32^3 | 1000 | coherent | 16361 | 31.7 |
| bresenham | 32^3 | 10000 | coherent | 16269 | 31.8 |
| bresenham | 32^3 | 1000 | axis_aligned | 16321 | 32.0 |
| bresenham | 32^3 | 10000 | axis_aligned | 16331 | 32.0 |
| bresenham | 64^3 | 1000 | uniform | 17854 | 23.7 |
| bresenham | 64^3 | 10000 | uniform | 17796 | 24.0 |
| bresenham | 64^3 | 1000 | coherent | 12241 | 63.5 |
| bresenham | 64^3 | 10000 | coherent | 12181 | 63.6 |
| bresenham | 64^3 | 1000 | axis_aligned | 12362 | 64.0 |
| bresenham | 64^3 | 10000 | axis_aligned | 12345 | 64.0 |
| bresenham | 128^3 | 1000 | uniform | 13678 | 47.6 |
| bresenham | 128^3 | 10000 | uniform | 13619 | 48.1 |
| bresenham | 128^3 | 1000 | coherent | 8024 | 127.0 |
| bresenham | 128^3 | 10000 | coherent | 8046 | 127.3 |
| bresenham | 128^3 | 1000 | axis_aligned | 8266 | 128.0 |
| bresenham | 128^3 | 10000 | axis_aligned | 8286 | 128.0 |
