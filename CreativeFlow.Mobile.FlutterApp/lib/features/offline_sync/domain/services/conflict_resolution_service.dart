import 'package:creativeflow_flutter_app/features/offline_sync/presentation/bloc/sync_cubit.dart';

// These are placeholder data models. In a real app, they would be more
// structured and likely part of the core domain layer.

/// Represents a change made locally while the application was offline.
class LocalChange {
  final String entityId;
  final DateTime timestamp;
  final dynamic data;
  LocalChange({required this.entityId, required this.timestamp, required this.data});
}

/// Represents a change made on the server that conflicts with a local change.
class ServerChange {
  final String entityId;
  final DateTime timestamp;
  final dynamic data;
  ServerChange({required this.entityId, required this.timestamp, required this.data});
}

/// Holds the outcome of the conflict resolution process.
class ResolutionResult {
  final bool hasConflicts;
  final List<Conflict> conflicts;
  final List<dynamic> mergedData; // Data that was merged successfully

  ResolutionResult({
    this.hasConflicts = false,
    this.conflicts = const [],
    this.mergedData = const [],
  });
}

/// Contains the business logic for handling data synchronization conflicts.
///
/// This service implements strategies for merging data, such as 'last-write-wins'
/// for simple cases, and flagging complex conflicts for manual user intervention.
abstract class ConflictResolutionService {
  /// Compares local and server changes to resolve discrepancies.
  ///
  /// Returns a [ResolutionResult] containing successfully merged data and
  /// any conflicts that could not be resolved automatically.
  Future<ResolutionResult> resolveConflicts({
    required List<LocalChange> localChanges,
    required List<ServerChange> serverChanges,
  });
}

/// The default implementation of the [ConflictResolutionService].
class ConflictResolutionServiceImpl implements ConflictResolutionService {
  @override
  Future<ResolutionResult> resolveConflicts({
    required List<LocalChange> localChanges,
    required List<ServerChange> serverChanges,
  }) async {
    final List<Conflict> foundConflicts = [];
    final List<dynamic> successfullyMergedData = [];

    // Use a map for efficient lookup of server changes by entity ID.
    final serverChangesMap = {for (var item in serverChanges) item.entityId: item};

    for (final localChange in localChanges) {
      final serverChange = serverChangesMap[localChange.entityId];

      if (serverChange != null) {
        // CONFLICT DETECTED: A change for the same entity exists on both client and server.

        // STRATEGY: Last-Write-Wins (based on timestamp).
        // This is a simple strategy suitable for non-collaborative data.
        if (localChange.timestamp.isAfter(serverChange.timestamp)) {
          // Local change is newer, so it "wins".
          successfullyMergedData.add(localChange.data);
        } else if (serverChange.timestamp.isAfter(localChange.timestamp)) {
          // Server change is newer, so it "wins".
          successfullyMergedData.add(serverChange.data);
        } else {
          // Timestamps are identical or a more complex merge is needed (e.g., for CRDTs).
          // We flag this as a conflict that requires user intervention.
          foundConflicts.add(Conflict(
            entityId: localChange.entityId,
            localData: localChange.data,
            remoteData: serverChange.data,
          ));
        }
        
        // Remove the processed server change from the map.
        serverChangesMap.remove(localChange.entityId);

      } else {
        // NO CONFLICT: This local change does not have a corresponding server change.
        // This could be a new entity created offline. It can be safely added.
        successfullyMergedData.add(localChange.data);
      }
    }

    // Any remaining items in `serverChangesMap` are new entities created on the
    // server while the client was offline. They should be added to the local state.
    successfullyMergedData.addAll(serverChangesMap.values.map((e) => e.data));

    return ResolutionResult(
      hasConflicts: foundConflicts.isNotEmpty,
      conflicts: foundConflicts,
      mergedData: successfullyMergedData,
    );
  }
}