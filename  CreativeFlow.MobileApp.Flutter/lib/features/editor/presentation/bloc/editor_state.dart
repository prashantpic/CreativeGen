part of 'editor_bloc.dart';

abstract class EditorState extends Equatable {
  const EditorState();
  
  @override
  List<Object> get props => [];
}

class EditorInitial extends EditorState {}

class EditorLoading extends EditorState {}

class EditorSaving extends EditorState {}

class EditorSaveSuccess extends EditorState {}

class EditorLoaded extends EditorState {
  final Map<String, dynamic> project;
  final List<Map<String, dynamic>> canvasElements;
  final bool isOffline;

  const EditorLoaded({
    required this.project,
    required this.canvasElements,
    this.isOffline = false,
  });

  EditorLoaded copyWith({
    Map<String, dynamic>? project,
    List<Map<String, dynamic>>? canvasElements,
    bool? isOffline,
  }) {
    return EditorLoaded(
      project: project ?? this.project,
      canvasElements: canvasElements ?? this.canvasElements,
      isOffline: isOffline ?? this.isOffline,
    );
  }

  @override
  List<Object> get props => [project, canvasElements, isOffline];
}

class EditorError extends EditorState {
  final String message;
  const EditorError({required this.message});

  @override
  List<Object> get props => [message];
}