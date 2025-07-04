import 'package:bloc/bloc.dart';
import 'package:creativeflow_flutter_app/core/database/app_database.dart';
import 'package:creativeflow_flutter_app/features/offline_sync/domain/services/conflict_resolution_service.dart';
import 'package:equatable/equatable.dart';

// In a real app, this would be a more complex object from the domain layer.
/// Represents a conflict between a local and a remote version of an entity.
class Conflict extends Equatable {
  final String entityId;
  final dynamic localData;
  final dynamic remoteData;

  const Conflict({required this.entityId, this.localData, this.remoteData});
  
  @override
  List<Object?> get props => [entityId, localData, remoteData];
}


// --------------- SYNC STATES ---------------

/// The base, abstract state for the data synchronization process.
abstract class SyncState extends Equatable {
  const SyncState();
  @override
  List<Object> get props => [];
}

/// The initial state before any synchronization has occurred.
class SyncInitial extends SyncState {}

/// Indicates that a synchronization process is currently in progress.
class SyncInProgress extends SyncState {}

/// Indicates that the synchronization completed successfully.
class SyncSuccess extends SyncState {
  final DateTime lastSynced;
  const SyncSuccess(this.lastSynced);
  @override
  List<Object> get props => [lastSynced];
}

/// Indicates that an error occurred during synchronization.
class SyncFailure extends SyncState {
  final String errorMessage;
  const SyncFailure(this.errorMessage);
  @override
  List<Object> get props => [errorMessage];
}

/// Indicates that conflicts were detected and require user intervention.
class SyncConflictDetected extends SyncState {
  final List<Conflict> conflicts;
  const SyncConflictDetected(this.conflicts);
  @override
  List<Object> get props => [conflicts];
}


// --------------- SYNC CUBIT ---------------

/// Manages the state for the data synchronization process.
///
/// This Cubit orchestrates the synchronization flow, communicates with domain
/// and data layer services, and emits states that the UI can react to,
/// such as showing progress indicators or conflict resolution dialogs.
class SyncCubit extends Cubit<SyncState> {
  // Dependencies are injected for testability.
  final ChangeQueueDao _changeQueueDao;
  final ConflictResolutionService _conflictResolutionService;
  // final YourApiClient _apiClient; // To communicate with the backend.

  SyncCubit(
    this._changeQueueDao, 
    this._conflictResolutionService,
    // this._apiClient,
  ) : super(SyncInitial());

  /// Initiates the data synchronization process.
  Future<void> startSync() async {
    try {
      emit(SyncInProgress());

      // 1. Fetch all unsynced changes from the local database queue.
      final queuedChanges = await _changeQueueDao.getQueuedChanges();
      
      // If there's nothing to sync, we're done.
      if (queuedChanges.isEmpty) {
        // Optionally, you could still fetch latest data from the server here.
        emit(SyncSuccess(DateTime.now()));
        return;
      }

      // Convert queued changes to a format the conflict resolver understands.
      final localChanges = queuedChanges.map((c) => LocalChange(
        entityId: c.payload['id'], // Assuming payload has an ID
        timestamp: c.timestamp, 
        data: c.payload,
      )).toList();

      // 2. Send changes to the backend and receive server-side changes in return.
      // final serverChanges = await _apiClient.syncChanges(localChanges);
      final serverChanges = <ServerChange>[]; // Placeholder for API response

      // 3. Invoke the conflict resolution service.
      final resolutionResult = await _conflictResolutionService.resolveConflicts(
        localChanges: localChanges,
        serverChanges: serverChanges
      );

      // 4. Check for conflicts that require manual resolution.
      if (resolutionResult.hasConflicts) {
        emit(SyncConflictDetected(resolutionResult.conflicts));
      } else {
        // 5. If successful, update the local database with the merged data.
        // await _updateLocalDatabase(resolutionResult.mergedData);

        // 6. Clear the change queue.
        await _changeQueueDao.clearQueue();

        // 7. Emit success state.
        emit(SyncSuccess(DateTime.now()));
      }
    } catch (e) {
      emit(SyncFailure(e.toString()));
    }
  }

  /// Handles manual resolution of a conflict by the user.
  Future<void> resolveConflictManually(/* ...params... */) async {
    // This method would take the user's choice (e.g., "keep local" or
    // "keep remote"), apply it, remove the conflict from the list, and
    // potentially resume the synchronization process if no other conflicts remain.
  }
}