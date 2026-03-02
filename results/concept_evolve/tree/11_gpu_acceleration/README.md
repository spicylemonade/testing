# CANVAS_RENDERER

Minimal HTML5 Canvas 2D renderer for real-time visualization. Maps simulation coordinates to screen coordinates with pan/zoom. Renders bodies as circles scaled by mass. Trail rendering for orbital paths.

## Mathematical Formalization

Screen transform: s = (x - camera.x) * zoom + canvas.width/2.  Circle radius: r_screen = max(2, log(mass) * scale).  Trail buffer: ring buffer of last K positions per body, rendered as polyline with alpha fade.

## Analogical Connections

- Canvas rendering loop <-> game engine update/render split (physics at fixed dt, render at display Hz)
- Trail rendering <-> time-series sparklines (recent history as a visual trace)
- Zoom/pan <-> coordinate transform in GIS (world coords -> screen coords)

## Implementation Hypothesis

requestAnimationFrame loop. Physics substeps at fixed dt inside render frame. Canvas clearRect + arc/fill for each body. Trail as a fading polyline. ~60 lines of rendering code, separate from physics.

## Experiment Seed

Render 50 random bodies with trails. Measure frame time. Should sustain 60fps. Add zoom with mouse wheel and pan with drag. Verify the visualization reveals structure (binary pairs, ejections) that raw data doesn't.
