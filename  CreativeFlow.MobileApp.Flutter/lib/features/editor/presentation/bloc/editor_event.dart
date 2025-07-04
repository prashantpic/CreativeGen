part of 'editor_bloc.dart';

abstract class EditorEvent extends Equatable {
  const EditorEvent();

  @override
  List<Object> get props => [];
}

class LoadEditorProject extends EditorEvent {
  final String projectId;
  const LoadEditorProject({required this.projectId});
  @override
  List<Object> get props => [projectId];
}

class SaveEditorProject extends EditorEvent {
  final Map<String, dynamic> projectData;
  const SaveEditorProject({required this.projectData});
  @override
  List<Object> get props => [projectData];
}

class AddElementToCanvas extends EditorEvent {
  final Map<String, dynamic> element;
  const AddElementToCanvas({required this.element});
  @override
  List<Object> get props => [element];
}

class UpdateElementOnCanvas extends EditorEvent {
  final Map<String, dynamic> element;
  const UpdateElementOnCanvas({required this.element});
  @override
  List<Object> get props => [element];
}

class DeleteElementFromCanvas extends EditorEvent {
  final String elementId;
  const DeleteElementFromCanvas({required this.elementId});
  @override
  List<Object> get props => [elementId];
}

class UndoCanvasChange extends EditorEvent {}

class RedoCanvasChange extends EditorEvent {}

class ApplyVoicePrompt extends EditorEvent {
  final String promptText;
  const ApplyVoicePrompt({required this.promptText});
  @override
  List<Object> get props => [promptText];
}

class MediaCaptured extends EditorEvent {
  final XFile mediaFile;
  final String type; // e.g., 'image', 'video'
  const MediaCaptured({required this.mediaFile, required this.type});
  @override
  List<Object> get props => [mediaFile, type];
}