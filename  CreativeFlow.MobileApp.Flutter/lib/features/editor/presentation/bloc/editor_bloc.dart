import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:creativeflow_mobileapp_flutter/core/bloc/connectivity_bloc.dart';
import 'package:creativeflow_mobileapp_flutter/core/services/sync_service.dart';
import 'package:equatable/equatable.dart';
import 'package:image_picker/image_picker.dart';

part 'editor_event.dart';
part 'editor_state.dart';

// --- Placeholder Classes for Compilation ---
class CreativeRepository {
  Future<Map<String, dynamic>> getProject(String id) async => {'id': id, 'name': 'Loaded Project'};
  Future<void> saveProjectRemote(Map<String, dynamic> data) async => Future.delayed(const Duration(seconds: 1));
}
// --- End Placeholder Classes ---


/// Manages the state and business logic for the creative editor feature.
///
/// This BLoC handles loading and saving projects, managing canvas elements,
/// and coordinating with the [SyncService] for offline operations.
class EditorBloc extends Bloc<EditorEvent, EditorState> {
  final CreativeRepository _creativeRepository;
  final SyncService _syncService;
  final ConnectivityBloc _connectivityBloc;
  
  EditorBloc({
    required CreativeRepository creativeRepository,
    required SyncService syncService,
    required ConnectivityBloc connectivityBloc,
  }) : _creativeRepository = creativeRepository,
       _syncService = syncService,
       _connectivityBloc = connectivityBloc,
       super(EditorInitial()) {
    on<LoadEditorProject>(_onLoadEditorProject);
    on<SaveEditorProject>(_onSaveEditorProject);
    on<AddElementToCanvas>(_onAddElementToCanvas);
    on<UpdateElementOnCanvas>(_onUpdateElementOnCanvas);
    on<DeleteElementFromCanvas>(_onDeleteElementFromCanvas);
    on<UndoCanvasChange>(_onUndoCanvasChange);
    on<RedoCanvasChange>(_onRedoCanvasChange);
    on<ApplyVoicePrompt>(_onApplyVoicePrompt);
    on<MediaCaptured>(_onMediaCaptured);
  }

  Future<void> _onLoadEditorProject(LoadEditorProject event, Emitter<EditorState> emit) async {
    emit(EditorLoading());
    try {
      // In a real app, this would check connectivity and load from local DB if offline.
      final projectData = await _creativeRepository.getProject(event.projectId);
      emit(EditorLoaded(
        project: projectData,
        canvasElements: const [], // Load elements from projectData
        isOffline: _connectivityBloc.state is ConnectivityOffline,
      ));
    } catch (e) {
      emit(EditorError(message: 'Failed to load project: ${e.toString()}'));
    }
  }

  Future<void> _onSaveEditorProject(SaveEditorProject event, Emitter<EditorState> emit) async {
    if (state is! EditorLoaded) return;
    final loadedState = state as EditorLoaded;

    emit(EditorSaving());
    
    final isOnline = _connectivityBloc.state is ConnectivityOnline;

    try {
      if (isOnline) {
        // If online, save directly to the remote server.
        await _creativeRepository.saveProjectRemote(event.projectData);
        emit(EditorSaveSuccess());
      } else {
        // If offline, queue the change using the SyncService.
        await _syncService.queueChange(
          entityType: 'project',
          entityId: loadedState.project['id'],
          operationType: 'update',
          payload: event.projectData,
        );
        emit(EditorSaveSuccess()); // Optimistically confirm save
      }
      // Re-emit loaded state to return UI to normal
      emit(loadedState.copyWith(isOffline: !isOnline)); 
    } catch (e) {
      emit(EditorError(message: 'Failed to save project: ${e.toString()}'));
      // Re-emit previous state on failure
      emit(loadedState);
    }
  }

  void _onAddElementToCanvas(AddElementToCanvas event, Emitter<EditorState> emit) {
    if (state is! EditorLoaded) return;
    final loadedState = state as EditorLoaded;
    final updatedElements = List.of(loadedState.canvasElements)..add(event.element);
    emit(loadedState.copyWith(canvasElements: updatedElements));
  }

  void _onUpdateElementOnCanvas(UpdateElementOnCanvas event, Emitter<EditorState> emit) {
    // Logic to find and update element in state
  }

  void _onDeleteElementFromCanvas(DeleteElementFromCanvas event, Emitter<EditorState> emit) {
    // Logic to find and remove element from state
  }

  void _onUndoCanvasChange(UndoCanvasChange event, Emitter<EditorState> emit) {
    // Logic to revert to a previous state from a history stack
  }



  void _onRedoCanvasChange(RedoCanvasChange event, Emitter<EditorState> emit) {
    // Logic to move forward in the history stack
  }

  void _onApplyVoicePrompt(ApplyVoicePrompt event, Emitter<EditorState> emit) {
    // Logic to process voice prompt and trigger AI generation or modifications
  }

  void _onMediaCaptured(MediaCaptured event, Emitter<EditorState> emit) {
    // Logic to add the captured media to the canvas as a new element
    final newMediaElement = {'type': 'image', 'path': event.mediaFile.path};
    add(AddElementToCanvas(element: newMediaElement));
  }
}