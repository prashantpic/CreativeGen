import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package.integration_test/integration_test.dart';
// Assuming the app has these components for testability.
import 'package:creative_flow_app/main.dart' as app;
import 'package:creative_flow_app/services/network_provider.dart';
import 'package:creative_flow_app/services/api_helper.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Offline Sync Journey', () {
    testWidgets('User can edit a project offline and sync changes upon reconnection', (tester) async {
      // Setup: Launch the app with a mockable network provider.
      // This requires the app to be architected to allow dependency injection.
      final mockNetworkProvider = MockNetworkProvider();
      app.main(networkProvider: mockNetworkProvider);
      await tester.pumpAndSettle();

      // 1. (Setup): Log in with an internet connection.
      mockNetworkProvider.setConnected(true);
      // ... (Login logic from auth_journey_test) ...
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pumpAndSettle(const Duration(seconds: 5));

      // 2. Navigate to a project and ensure it's loaded.
      await tester.tap(find.byKey(const Key('project_item_1')));
      await tester.pumpAndSettle();
      expect(find.byKey(const Key('editor_canvas')), findsOneWidget);
      
      const originalText = 'Initial Text';
      expect(find.text(originalText), findsOneWidget);

      // 3. (Mock network disconnection)
      mockNetworkProvider.setConnected(false);
      debugPrint("Network connection is now OFF");

      // 4. Find a text element on the canvas and tap it to edit.
      await tester.tap(find.text(originalText));
      await tester.pumpAndSettle();

      // 5. Enter new text.
      const offlineEditText = 'Edited Offline Text';
      await tester.enterText(find.byKey(const Key('text_editor_input')), offlineEditText);
      await tester.tap(find.byKey(const Key('text_editor_save_button')));
      await tester.pumpAndSettle();

      // 6. Assert that the local UI reflects the change.
      expect(find.text(offlineEditText), findsOneWidget);
      expect(find.text(originalText), findsNothing);

      // 7. (Mock network reconnection).
      mockNetworkProvider.setConnected(true);
      debugPrint("Network connection is now ON");

      // 8. Trigger the sync process (e.g., by a button or automatically).
      // Assuming the app has a sync button for testing or an automatic trigger.
      await tester.tap(find.byKey(const Key('sync_now_button')));
      
      // 9. `await tester.pumpAndSettle();` to wait for sync to complete.
      await tester.pumpAndSettle(const Duration(seconds: 10)); // Allow time for API call

      // 10. (Verification): Use an API helper to fetch the project state from the backend.
      final projectId = 'project_id_123'; // The ID of the project being edited.
      final projectState = await ApiHelper.getProjectState(projectId);
      
      // Assert that the changes are present in the backend data.
      expect(projectState.contains(offlineEditText), isTrue);
    });
  });
}