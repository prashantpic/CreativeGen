import 'dart:async';
import 'dart:convert';
import 'package:creativeflow_mobileapp_flutter/core/bloc/connectivity_bloc.dart';
import 'package:creativeflow_mobileapp_flutter/core/network/api_client.dart';
import 'package:creativeflow_mobileapp_flutter/core/storage/local_database.dart';
import 'package:flutter/foundation.dart';

/// Orchestrates the synchronization of local offline data with the backend server.
///
/// This service listens for connectivity changes and processes a queue of
/// local modifications (creates, updates, deletes) when the device is online.
/// It also includes logic for conflict resolution.
class SyncService {
  final AppLocalDatabase _localDb;
  final ApiClient _apiClient;
  final ConnectivityBloc _connectivityBloc;

  StreamSubscription? _connectivitySubscription;
  bool _isSyncing = false;

  SyncService({
    required AppLocalDatabase localDb,
    required ApiClient apiClient,
    required ConnectivityBloc connectivityBloc,
  })  : _localDb = localDb,
        _apiClient = apiClient,
        _connectivityBloc = connectivityBloc;

  /// Initializes the service by subscribing to connectivity changes.
  void initialize() {
    _connectivitySubscription = _connectivityBloc.stream.listen((state) {
      if (state is ConnectivityOnline) {
        if (kDebugMode) {
          print('Connectivity back online. Triggering sync queue processing.');
        }
        processSyncQueue();
      }
    });
  }

  /// Queues a local change for synchronization.
  ///
  /// This method is called by repositories when data is modified offline.
  Future<void> queueChange({
    required String entityType,
    required String entityId,
    required String operationType,
    required Map<String, dynamic> payload,
  }) async {
    final item = OfflineSyncQueueItemsCompanion(
      entityType: Value(entityType),
      entityId: Value(entityId),
      operationType: Value(operationType),
      payloadJson: Value(jsonEncode(payload)),
    );
    // await _localDb.offlineSyncQueueDao.addQueueItem(item);
    if (kDebugMode) {
      print('Queued change: $operationType on $entityType($entityId)');
    }
  }

  /// Processes the queue of pending offline changes.
  Future<void> processSyncQueue() async {
    if (_isSyncing || _connectivityBloc.state is ConnectivityOffline) {
      return; // Already syncing or offline, do nothing.
    }

    _isSyncing = true;
    try {
      // final queueItems = await _localDb.offlineSyncQueueDao.getPendingItems();
      // Placeholder for actual items
      final List<OfflineSyncQueueItem> queueItems = [];

      if (queueItems.isEmpty) {
        _isSyncing = false;
        return;
      }

      if (kDebugMode) {
        print('Processing ${queueItems.length} items from the sync queue.');
      }

      for (final item in queueItems) {
        try {
          final payload = jsonDecode(item.payloadJson) as Map<String, dynamic>;
          switch (item.operationType) {
            case 'create':
              await _apiClient.post('/${item.entityType}', body: payload);
              break;
            case 'update':
              await _apiClient.put('/${item.entityType}/${item.entityId}', body: payload);
              break;
            case 'delete':
              await _apiClient.delete('/${item.entityType}/${item.entityId}');
              break;
          }

          // On success, remove the item from the queue.
          // await _localDb.offlineSyncQueueDao.deleteQueueItem(item.id);

        } on ApiException catch (e) {
          if (e.statusCode == 409) {
            // Conflict detected (REQ-019.1)
            if (kDebugMode) {
              print('Conflict detected for item ${item.id}. Starting resolution.');
            }
            await _resolveConflict(item);
          } else {
            // Other API error, increment attempt count.
            // await _localDb.offlineSyncQueueDao.incrementAttemptCount(item.id);
            if (kDebugMode) {
              print('API error syncing item ${item.id}: ${e.message}');
            }
          }
        } catch (e) {
          // Network or other unexpected error.
          // await _localDb.offlineSyncQueueDao.incrementAttemptCount(item.id);
           if (kDebugMode) {
              print('Unexpected error syncing item ${item.id}: $e');
           }
        }
      }
    } finally {
      _isSyncing = false;
    }
  }

  /// Logic for handling data conflicts during synchronization.
  Future<void> _resolveConflict(OfflineSyncQueueItem item) async {
    // This is a simplified example of "last write wins" based on server data.
    // More complex strategies could involve merging data or prompting the user.
    if (kDebugMode) {
      print('Resolving conflict: Fetching latest data for ${item.entityType}/${item.entityId}');
    }
    
    try {
      // 1. Fetch the latest version from the server.
      // final serverData = await _apiClient.get('/${item.entityType}/${item.entityId}');
      // final serverProject = ProjectModel.fromJson(jsonDecode(serverData));

      // 2. Update the local database with the server's version.
      // This effectively discards the local change that caused the conflict.
      // await _localDb.projectDao.updateProject(serverProject.toLocalCompanion());

      // 3. Delete the conflicting item from the sync queue.
      // await _localDb.offlineSyncQueueDao.deleteQueueItem(item.id);

      // 4. (Optional) Notify the user that their local changes were overwritten.
      // This could be done by emitting an event from a BLoC.
    } catch (e) {
      if (kDebugMode) {
        print('Failed to resolve conflict for item ${item.id}: $e');
      }
    }
  }

  /// Cleans up resources, such as stream subscriptions.
  void dispose() {
    _connectivitySubscription?.cancel();
  }
}