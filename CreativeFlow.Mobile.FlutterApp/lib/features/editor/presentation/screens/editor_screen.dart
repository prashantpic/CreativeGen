import 'package:creativeflow_flutter_app/app/widgets/network_status_indicator.dart';
import 'package:creativeflow_flutter_app/features/editor/presentation/widgets/canvas_gesture_detector.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// Placeholder for EditorCubit and EditorState. In a real application, these
// would be in their own files within the BLoC structure.
class EditorCubit extends Cubit<EditorState> {
  EditorCubit() : super(const EditorState());

  void selectObjectAt(Offset position) {
    // Logic to update state when an object is selected
  }
  void panCanvas(Offset delta) {
    // Logic to update the canvas transform state
  }
}

class EditorState extends Equatable {
  const EditorState();
  @override
  List<Object> get props => [];
}

/// The main screen for the creative editor.
///
/// This screen provides a touch-optimized UI for creating and editing visual
/// content. It's composed of a central canvas, overlaid toolbars, and uses a
/// `BlocProvider` to manage the editor's state.
class EditorScreen extends StatelessWidget {
  final String projectId;

  const EditorScreen({super.key, required this.projectId});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => EditorCubit(), // In a real app, you might load the project here.
      child: Scaffold(
        // The NetworkStatusIndicator can be wrapped around the Scaffold's body
        // to show an offline banner without obscuring the AppBar.
        body: NetworkStatusIndicator(
          child: SafeArea(
            bottom: false, // Let the bottom palette handle safe area
            child: Column(
              children: [
                _TopToolbar(projectId: projectId),
                const Expanded(
                  child: Stack(
                    children: [
                      // The main interactive canvas area
                      CanvasGestureDetector(),
                      // Other overlay widgets like rulers or guides could go here.
                    ],
                  ),
                ),
                const _BottomToolPalette(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// The top toolbar containing project-level actions.
class _TopToolbar extends StatelessWidget {
  final String projectId;
  const _TopToolbar({required this.projectId});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0),
      height: kToolbarHeight,
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border(bottom: BorderSide(color: Colors.grey.shade300, width: 0.5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new),
            onPressed: () => Navigator.of(context).pop(),
          ),
          Text(
            'Editing Project', // A more descriptive name would be used
            style: Theme.of(context).textTheme.titleMedium,
          ),
          ElevatedButton.icon(
            icon: const Icon(Icons.save_alt),
            label: const Text('Save'),
            onPressed: () {
              // Trigger save logic in the EditorCubit
            },
          ),
        ],
      ),
    );
  }
}

/// The bottom palette containing tools for editing the canvas.
class _BottomToolPalette extends StatelessWidget {
  const _BottomToolPalette();

  @override
  Widget build(BuildContext context) {
    return Material(
      elevation: 4.0,
      color: Theme.of(context).colorScheme.surface,
      child: SafeArea(
        top: false, // We are at the bottom
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _ToolIcon(icon: Icons.text_fields, label: 'Text'),
              _ToolIcon(icon: Icons.image_outlined, label: 'Image'),
              _ToolIcon(icon: Icons.shape_line_outlined, label: 'Shapes'),
              _ToolIcon(icon: Icons.color_lens_outlined, label: 'Colors'),
              _ToolIcon(icon: Icons.layers_outlined, label: 'Layers'),
            ],
          ),
        ),
      ),
    );
  }
}

class _ToolIcon extends StatelessWidget {
  final IconData icon;
  final String label;
  const _ToolIcon({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {},
      borderRadius: BorderRadius.circular(8),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon),
            const SizedBox(height: 4),
            Text(label, style: Theme.of(context).textTheme.labelSmall),
          ],
        ),
      ),
    );
  }
}