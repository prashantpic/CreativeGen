import 'package:creativeflow_flutter_app/features/editor/presentation/screens/editor_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

/// A specialized widget that wraps the creative canvas.
///
/// It handles all touch-based gestures like pinch-to-zoom, pan, and tap,
/// translating user touch input into commands for the [EditorCubit] to manage
/// the editor's state. It also contains the `CustomPaint` widget responsible
/// for rendering the canvas content.
class CanvasGestureDetector extends StatelessWidget {
  const CanvasGestureDetector({super.key});

  @override
  Widget build(BuildContext context) {
    // Reading the cubit once to pass to gesture callbacks.
    // This avoids repeatedly calling context.read inside the callbacks.
    final editorCubit = context.read<EditorCubit>();

    return GestureDetector(
      // --- GESTURE CALLBACKS ---

      onTapDown: (details) {
        // User tapped on the canvas.
        // The cubit will handle the logic to determine if an object was hit.
        editorCubit.selectObjectAt(details.localPosition);
      },

      onPanUpdate: (details) {
        // User is dragging a finger across the screen.
        // The cubit will decide whether to move a selected object or pan the entire canvas.
        editorCubit.panCanvas(details.delta);
      },

      onScaleUpdate: (details) {
        // User is pinching with two fingers.
        // The cubit will handle resizing a selected object or zooming the canvas.
        // This requires more complex state management in the cubit.
        // editorCubit.scaleCanvas(details.scale, details.localFocalPoint);
      },

      // --- CANVAS RENDERING ---

      // The child is a BlocBuilder that listens to EditorState changes.
      // Whenever the state changes (e.g., an object is moved), this builder
      // will trigger a repaint of the CustomPaint widget.
      child: BlocBuilder<EditorCubit, EditorState>(
        builder: (context, state) {
          return Container(
            // A background color for the canvas area.
            color: Colors.grey.shade200,
            // Occupy all available space within the parent Stack.
            width: double.infinity,
            height: double.infinity,
            // The CustomPaint widget is where the actual drawing happens.
            child: CustomPaint(
              painter: _CanvasPainter(state),
            ),
          );
        },
      ),
    );
  }
}

/// A CustomPainter that renders the visual content of the editor.
class _CanvasPainter extends CustomPainter {
  final EditorState state;

  _CanvasPainter(this.state);

  @override
  void paint(Canvas canvas, Size size) {
    // In a real implementation, this method would be much more complex.
    // It would:
    // 1. Get the current canvas transform (pan, zoom) from the EditorState.
    // 2. Apply the transform to the canvas: canvas.translate(...); canvas.scale(...);
    // 3. Iterate through a list of creative objects from the EditorState.
    //    e.g., for (final creativeObject in state.objects) { ... }
    // 4. For each object, call its specific drawing method.
    //    e.g., if it's an image, use canvas.drawImage.
    //    e.g., if it's text, use a TextPainter to draw it.

    // This is a placeholder drawing to visualize the canvas area.
    final textPainter = TextPainter(
      text: const TextSpan(
        text: 'Interactive Canvas',
        style: TextStyle(color: Colors.black54, fontSize: 24),
      ),
      textDirection: TextDirection.ltr,
    );
    textPainter.layout();
    final offset = Offset(
      (size.width - textPainter.width) / 2,
      (size.height - textPainter.height) / 2,
    );
    textPainter.paint(canvas, offset);

    // Draw a sample object.
    final objectPaint = Paint()
      ..color = Colors.deepPurpleAccent
      ..style = PaintingStyle.fill;
    canvas.drawCircle(const Offset(120, 150), 30, objectPaint);
  }

  @override
  bool shouldRepaint(covariant _CanvasPainter oldDelegate) {
    // The canvas should only repaint if the editor state has changed.
    // Using Equatable on the EditorState makes this comparison efficient.
    return oldDelegate.state != state;
  }
}