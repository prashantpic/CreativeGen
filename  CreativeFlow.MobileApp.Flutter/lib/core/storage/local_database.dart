import 'dart:io';
import 'package:creativeflow_mobileapp_flutter/core/constants/app_constants.dart';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

// DAOs will be defined in their respective feature directories and imported here.
// e.g., import '../../features/editor/data/datasources/daos/project_dao.dart';
// e.g., import '../../features/editor/data/datasources/daos/asset_dao.dart';
// e.g., import '../../features/sync/data/datasources/daos/offline_sync_queue_dao.dart';

part 'local_database.g.dart';

// --- Table Definitions ---

/// Stores project metadata for offline access.
@DataClassName('LocalProject')
class LocalProjects extends Table {
  TextColumn get id => text()();
  TextColumn get workbenchId => text()();
  TextColumn get name => text()();
  TextColumn get collaborationStateJson => text().nullable()();
  DateTimeColumn get lastSyncedAt => dateTime().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get updatedAt => dateTime().withDefault(currentDateAndTime)();
  BoolColumn get isSynced => boolean().withDefault(const Constant(false))();

  @override
  Set<Column> get primaryKey => {id};
}

/// Stores asset metadata and local file paths for offline assets.
@DataClassName('LocalAsset')
class LocalAssets extends Table {
  TextColumn get id => text()();
  TextColumn get projectId => text().nullable().references(LocalProjects, #id)();
  TextColumn get name => text()();
  TextColumn get localPath => text()();
  TextColumn get remotePath => text().nullable()();
  TextColumn get mimeType => text()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  BoolColumn get isSynced => boolean().withDefault(const Constant(false))();
  
  @override
  Set<Column> get primaryKey => {id};
}

/// Queues local changes that need to be synchronized with the backend.
@DataClassName('OfflineSyncQueueItem')
class OfflineSyncQueueItems extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get entityType => text()();
  TextColumn get entityId => text()();
  TextColumn get operationType => text()();
  TextColumn get payloadJson => text()();
  DateTimeColumn get queuedAt => dateTime().withDefault(currentDateAndTime)();
  IntColumn get attemptCount => integer().withDefault(const Constant(0))();
}


/// The main database class for the application.
///
/// This class, annotated with `@DriftDatabase`, brings together all the tables
/// and DAOs. Drift will generate the necessary code to interact with the
-/// underlying SQLite database.
@DriftDatabase(
  tables: [LocalProjects, LocalAssets, OfflineSyncQueueItems],
  // DAOs are defined in feature directories to keep data access logic
  // co-located with the features that use it. They will be added here
  // once defined.
  // Example:
  // daos: [ProjectDao, AssetDao, OfflineSyncQueueDao],
)
class AppLocalDatabase extends _$AppLocalDatabase {
  AppLocalDatabase() : super(_openConnection());

  @override
  int get schemaVersion => AppConstants.localDbVersion;

  @override
  MigrationStrategy get migration => MigrationStrategy(
        onCreate: (Migrator m) async {
          await m.createAll();
        },
        onUpgrade: (Migrator m, int from, int to) async {
          // Handle schema migrations here.
          // Example:
          // if (from < 2) {
          //   await m.addColumn(localProjects, localProjects.someNewColumn);
          // }
        },
      );
}

/// Opens the database connection.
///
/// It finds the correct location for the database file on the device
/// and creates a [NativeDatabase] connection.
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, AppConstants.localDbName));
    return NativeDatabase.createInBackground(file);
  });
}