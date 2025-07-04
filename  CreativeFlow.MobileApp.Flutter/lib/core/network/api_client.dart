import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

// --- Placeholder Classes for Compilation ---
class AuthTokenRepository {
  Future<String?> getAuthToken() async => 'dummy-jwt-token';
  Future<void> refreshToken() async {}
}
// --- End Placeholder Classes ---

/// A client for making HTTP requests to the CreativeFlow backend API.
///
/// This class centralizes network request logic, including adding
/// authentication headers, handling responses, and throwing typed
/// exceptions for different error scenarios.
class ApiClient {
  final http.Client _client;
  final String _baseUrl;
  final AuthTokenRepository _authTokenRepository;

  ApiClient({
    required http.Client client,
    required String baseUrl,
    required AuthTokenRepository authTokenRepository,
  })  : _client = client,
        _baseUrl = baseUrl,
        _authTokenRepository = authTokenRepository;

  /// Performs a GET request.
  Future<String> get(String path, {Map<String, String>? queryParameters}) async {
    final headers = await _getHeaders();
    final uri = Uri.parse('$_baseUrl$path').replace(queryParameters: queryParameters);
    
    final response = await _client.get(uri, headers: headers);
    return _handleResponse(response);
  }

  /// Performs a POST request.
  Future<String> post(String path, {required Map<String, dynamic> body}) async {
    final headers = await _getHeaders();
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.post(uri, headers: headers, body: jsonEncode(body));
    return _handleResponse(response);
  }

  /// Performs a PUT request.
  Future<String> put(String path, {required Map<String, dynamic> body}) async {
    final headers = await _getHeaders();
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.put(uri, headers: headers, body: jsonEncode(body));
    return _handleResponse(response);
  }

  /// Performs a DELETE request.
  Future<String> delete(String path, {Map<String, dynamic>? body}) async {
    final headers = await _getHeaders();
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.delete(uri, headers: headers, body: body != null ? jsonEncode(body) : null);
    return _handleResponse(response);
  }


  /// Constructs the default headers for an API request.
  ///
  /// Includes the `Content-Type`, `Accept`, and `Authorization` headers if required.
  Future<Map<String, String>> _getHeaders({bool requiresAuth = true}) async {
    final headers = {
      'Content-Type': 'application/json; charset=UTF-8',
      'Accept': 'application/json',
    };

    if (requiresAuth) {
      final token = await _authTokenRepository.getAuthToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }
    return headers;
  }

  /// Handles the HTTP response, checking status codes and throwing exceptions.
  String _handleResponse(http.Response response) {
    final statusCode = response.statusCode;
    if (statusCode >= 200 && statusCode < 300) {
      // Successful response
      return response.body;
    } else {
      // Unsuccessful response, throw a typed exception.
      final responseBody = jsonDecode(response.body);
      final message = responseBody['message'] ?? 'An unknown error occurred.';
      
      switch (statusCode) {
        case 400:
          throw BadRequestException(message, statusCode);
        case 401:
        case 403:
          throw UnauthorizedException(message, statusCode);
        case 404:
          throw NotFoundException(message, statusCode);
        case 500:
        default:
          throw ApiException(message, statusCode);
      }
    }
  }
}

// --- Custom Exception Classes ---

/// Base class for all API-related exceptions.
class ApiException implements Exception {
  final String message;
  final int statusCode;
  ApiException(this.message, this.statusCode);
  @override
  String toString() => 'ApiException: $statusCode - $message';
}

/// Thrown for 400 Bad Request errors.
class BadRequestException extends ApiException {
  BadRequestException(String message, int statusCode) : super(message, statusCode);
}

/// Thrown for 401 Unauthorized or 403 Forbidden errors.
class UnauthorizedException extends ApiException {
  UnauthorizedException(String message, int statusCode) : super(message, statusCode);
}

/// Thrown for 404 Not Found errors.
class NotFoundException extends ApiException {
  NotFoundException(String message, int statusCode) : super(message, statusCode);
}