/// Central repository for all named route paths used in the application.
///
/// Using this class prevents typos and provides a single source of truth for
/// navigation routes, making the codebase more maintainable.
class RoutePaths {
  // Private constructor to prevent instantiation.
  RoutePaths._();

  /// The initial route, typically showing a splash screen.
  static const String splash = '/';

  /// Route for the user login screen.
  static const String login = '/login';

  /// Route for the user registration screen.
  static const String register = '/register';

  /// The main screen after login, typically the dashboard or home screen.
  static const String home = '/home';

  /// The creative editor screen. Expects a project ID as an argument.
  /// Example: `/editor/project-123`
  static const String editor = '/editor';

  /// Screen showing details of a specific project. Expects a project ID.
  static const String projectDetails = '/project';

  /// Screen showing details of a specific workbench. Expects a workbench ID.
  static const String workbenchDetails = '/workbench';

  /// The main settings screen.
  static const String settings = '/settings';

  /// Screen for managing user account settings.
  static const String accountSettings = '/settings/account';

  /// Screen for configuring accessibility options.
  /// Requirement: UI-005
  static const String accessibilitySettings = '/settings/accessibility';

  /// Screen listing all available brand kits.
  static const String brandKitList = '/brand-kits';

  /// Screen showing details of a specific brand kit. Expects a kit ID.
  static const String brandKitDetails = '/brand-kit';

  /// Screen displaying the gallery of creative templates.
  static const String templateGallery = '/templates';
}