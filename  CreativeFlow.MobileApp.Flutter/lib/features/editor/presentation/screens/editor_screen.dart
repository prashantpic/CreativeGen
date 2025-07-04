import 'package:creativeflow_mobileapp_flutter/features/editor/presentation/bloc/editor_bloc.dart';
import 'package:creativeflow_mobileapp_flutter/features/editor/presentation/widgets/camera_input_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:image_picker/image_picker.dart';

// --- Placeholder Widgets for Compilation ---
class CanvasWidget extends StatelessWidget { const CanvasWidget({super.key}); @override Widget build(BuildContext context) => Container(color: Colors.grey[200], child: const Center(child: Text('Canvas Area'))); }
class ToolPaletteWidget extends StatelessWidget { const ToolPaletteWidget({super.key}); @override Widget build(BuildContext context) => Container(color: Colors.blueGrey[100], height: 60, child: const Center(child: Text('Tool Palette'))); }
class AssetPickerWidget extends StatelessWidget { const AssetPickerWidget({super.key}); @override Widget build(BuildContext context) => Container(color: Colors.blueGrey[100], height: 80, child: const Center(child: Text('Asset Picker'))); }
class VoiceInputWidget extends StatelessWidget { const VoiceInputWidget({super.key}); @override Widget build(BuildContext context) => IconButton(icon: const Icon(Icons.mic), onPressed: () {}); }
// --- End Placeholder Widgets ---

/// The main screen for the creative editor.
///
/// This screen hosts the canvas for editing, tool palettes, and asset pickers.
/// It manages its state via the [EditorBloc] and implements touch-optimized
/// workflows for mobile interactions.
class EditorScreen extends StatefulWidget {
  final String projectId;

  const EditorScreen({super.key, required this.projectId});

  @override
  State<EditorScreen> createState() => _EditorScreenState();
}

class _EditorScreenState extends State<EditorScreen> {
  @override
  void initState() {
    super.initState();
    // Load the project data when the screen is initialized.
    // This assumes EditorBloc is provided by a parent widget (e.g., via AppRouter).
    // For a standalone screen, you would provide it here.
    context.read<EditorBloc>().add(LoadEditorProject(projectId: widget.projectId));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Creative Editor'),
        actions: [
          IconButton(
            icon: const Icon(Icons.undo),
            onPressed: () => context.read<EditorBloc>().add(UndoCanvasChange()),
          ),
          IconButton(
            icon: const Icon(Icons.redo),
            onPressed: () => context.read<EditorBloc>().add(RedoCanvasChange()),
          ),
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: () {
              // In a real app, you would pass the current project state.
              // final currentState = context.read<EditorBloc>().state;
              // if (currentState is EditorLoaded) { ... }
              context.read<EditorBloc>().add(SaveEditorProject(projectData: {}));
            },
          ),
        ],
      ),
      body: BlocConsumer<EditorBloc, EditorState>(
        listener: (context, state) {
          // Handle side effects like showing SnackBars for different states.
          if (state is EditorSaveSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Project saved successfully!'), backgroundColor: Colors.green),
            );
          } else if (state is EditorError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Error: ${state.message}'), backgroundColor: Colors.red),
            );
          }
        },
        builder: (context, state) {
          // Build the UI based on the current state of the EditorBloc.
          if (state is EditorLoading || state is EditorInitial) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is EditorError) {
            return Center(child: Text('Failed to load project: ${state.message}'));
          }
          if (state is EditorLoaded) {
            // Main editor layout
            return Column(
              children: [
                Expanded(
                  child: GestureDetector(
                    // These gestures would dispatch events to the EditorBloc
                    // to manipulate elements on the canvas.
                    onPanUpdate: (details) {
                      // context.read<EditorBloc>().add(DragElementEvent(details));
                    },
                    onScaleUpdate: (details) {
                      // context.read<EditorBloc>().add(ScaleElementEvent(details));
                    },
                    onTap: () {
                      // context.read<EditorBloc>().add(SelectElementEvent());
                    },
                    child: const CanvasWidget(),
                  ),
                ),
                const ToolPaletteWidget(),
                const AssetPickerWidget(),
                // Buttons for native feature integrations (REQ-020)
                _buildFeatureButtons(context),
              ],
            );
          }
          return const Center(child: Text('An unexpected error occurred.'));
        },
      ),
    );
  }

  Widget _buildFeatureButtons(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          CameraInputWidget(
            onMediaCaptured: (XFile mediaFile) {
              context.read<EditorBloc>().add(MediaCaptured(mediaFile: mediaFile, type: 'image'));
            },
          ),
          const VoiceInputWidget(),
        ],
      ),
    );
  }
}