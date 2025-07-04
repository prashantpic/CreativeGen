import 'dart:convert';
import 'dart.io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'app_database.g.dart';

// --------------- ENUMS AND TYPE CONVERTERS ---------------

/// Synchronization status for offline entities.
enum SyncStatus { synced, pending, conflict }

/// Type of a creative asset.
enum AssetType { image, video, text, unknown }

/// A Drift type converter for storing JSON objects as text.
class JsonConverter extends TypeConverter<Map<String, dynamic>, String> {
  const JsonConverter();
  @override
  Map<String, dynamic> fromSql(String fromDb) {
    return json.decode(fromDb) as Map<String, dynamic>;
  }

  @override
  String toSql(Map<String, dynamic> value) {
    return json.encode(value);
  }
}


// --------------- TABLE DEFINITIONS ---------------

/// Caches project data for offline access.
@DataClassName('OfflineProject')
class OfflineProjects extends Table {
  @override
  String get tableName => 'offline_projects';

  TextColumn get id => text().customConstraint('PRIMARY KEY')();
  TextColumn get name => text()();
  TextColumn get workbenchId => text()();
  DateTimeColumn get lastModified => dateTime()();
  IntColumn get syncStatus => intEnum<SyncStatus>()();
  TextColumn get data => text().map(const JsonConverter())(); // Full project data as JSON
}

/// Caches asset metadata and local file paths.
@DataClassName('OfflineAsset')
class OfflineAssets extends Table {
  @override
  String get tableName => 'offline_assets';

  TextColumn get id => text().customConstraint('PRIMARY KEY')();
  TextColumn get projectId => text().references(OfflineProjects, #id)();
  TextColumn get name => text()();
  TextColumn get localPath => text()();
  TextColumn get remoteUrl => text().nullable()();
  IntColumn get type => intEnum<AssetType>()();
  DateTimeColumn get lastModified => dateTime()();
}

/// A log of user actions performed offline that need to be sent to the server.
@DataClassName('QueuedChange')
class QueuedChanges extends Table {
  @override
  String get tableName => 'queued_changes';

  IntColumn get id => integer().autoIncrement()();
  DateTimeColumn get timestamp => dateTime()();
  TextColumn get actionType => text().withLength(min: 1, max: 50)(); // e.g., 'update_project'
  TextColumn get payload => text().map(const JsonConverter())(); // JSON payload for the action
}


// --------------- DATABASE CLASS ---------------

/// The main database class for the application, defined using Drift.
///
/// This class specifies the tables and DAOs (Data Access Objects) that
/// are part of the local SQLite database. The `drift_dev` package generates
/// the necessary code in the `.g.dart` part file.
@DriftDatabase(
  tables: [OfflineProjects, OfflineAssets, QueuedChanges],
  daos: [ProjectDao, AssetDao, ChangeQueueDao],
)
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  AppDatabase.forTesting(DatabaseConnection connection) : super(connection);

  @override
  int get schemaVersion => 1;
}

/// Opens the database connection.
///
/// This function determines the correct location for the database file on the
/// device's filesystem and creates a `NativeDatabase`.
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'creativeflow.db.sqlite'));
    return NativeDatabase.createInBackground(file);
  });
}


// --------------- DATA ACCESS OBJECTS (DAOs) ---------------

/// Provides type-safe methods for interacting with the `offline_projects` table.
@DriftAccessor(tables: [OfflineProjects])
class ProjectDao extends DatabaseAccessor<AppDatabase> with _$ProjectDaoMixin {
  ProjectDao(AppDatabase db) : super(db);

  Future<List<OfflineProject>> getAllProjects() => select(offlineProjects).get();
  Future<void> upsertProject(OfflineProject project) => into(offlineProjects).insertOnConflictUpdate(project);
}

/// Provides type-safe methods for interacting with the `offline_assets` table.
@DriftAccessor(tables: [OfflineAssets])
class AssetDao extends DatabaseAccessor<AppDatabase> with _$AssetDaoMixin {
  AssetDao(AppDatabase db) : super(db);

  Future<List<OfflineAsset>> getAssetsForProject(String projectId) {
    return (select(offlineAssets)..where((tbl) => tbl.projectId.equals(projectId))).get();
  }
  Future<void> upsertAsset(OfflineAsset asset) => into(offlineAssets).insertOnConflictUpdate(asset);
}

/// Provides methods to manage the queue of offline changes.
@DriftAccessor(tables: [QueuedChanges])
class ChangeQueueDao extends DatabaseAccessor<AppDatabase> with _$ChangeQueueDaoMixin {
  ChangeQueueDao(AppDatabase db) : super(db);

  Future<void> enqueueChange(QueuedChangesCompanion change) => into(queuedChanges).insert(change);
  Future<List<QueuedChange>> getQueuedChanges() => select(queuedChanges).get();
  Future<void> deleteChange(int id) => (delete(queuedChanges)..where((tbl) => tbl.id.equals(id))).go();
  Future<void> clearQueue() => delete(queuedChanges).go();
}