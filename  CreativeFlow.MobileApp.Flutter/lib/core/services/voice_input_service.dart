import 'package:creativeflow_mobileapp_flutter/core/services/permission_handler_service.dart';
import 'package:flutter/foundation.dart';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';

/// Provides voice-to-text functionality for inputting creative prompts (REQ-020).
///
/// This service abstracts the `speech_to_text` plugin, handling initialization,
/// permissions, and the listening lifecycle.
class VoiceInputService {
  final SpeechToText _speechToText = SpeechToText();
  bool _isInitialized = false;
  bool _isListening = false;
  String _lastRecognizedWords = "";

  /// Public getter to check if the service is currently listening for speech.
  bool get isListening => _isListening;

  /// Public getter for the last string of recognized words.
  String get lastWords => _lastRecognizedWords;

  /// Initializes the speech-to-text service.
  ///
  /// This must be called before any other methods. It requests microphone
  /// permission and prepares the underlying plugin. Returns `true` if
  /// initialization is successful.
  Future<bool> initialize() async {
    final permissionStatus = await PermissionHandlerService.requestMicrophonePermission();
    if (!permissionStatus.isGranted) {
      if (kDebugMode) {
        print('Microphone permission not granted.');
      }
      return false;
    }

    if (_isInitialized) return true;

    _isInitialized = await _speechToText.initialize(
      onError: _onError,
      onStatus: _onStatus,
    );
    return _isInitialized;
  }

  /// Starts listening for speech.
  ///
  /// [onResult] is a callback that will be invoked with the recognized text.
  /// [onStatusChange] is a callback that provides the current listening status.
  void startListening({
    required Function(String words) onResult,
  }) {
    if (!_isInitialized || _speechToText.isListening) {
      return;
    }

    _lastRecognizedWords = "";
    _speechToText.listen(
      onResult: (SpeechRecognitionResult result) {
        _lastRecognizedWords = result.recognizedWords;
        onResult(_lastRecognizedWords);
        if (result.finalResult) {
          _isListening = false;
        }
      },
      listenFor: const Duration(seconds: 30),
      localeId: 'en_US', // Can be made configurable
      onDevice: true, // Prefer on-device recognition for speed and offline capability
    );
    _isListening = true;
  }

  /// Stops the current listening session.
  void stopListening() {
    if (!_speechToText.isListening) return;
    _speechToText.stop();
    _isListening = false;
  }

  /// Cancels the current listening session without returning a result.
  void cancelListening() {
    if (!_speechToText.isListening) return;
    _speechToText.cancel();
    _isListening = false;
  }

  /// Callback for handling errors from the speech recognition engine.
  void _onError(SpeechRecognitionError error) {
    if (kDebugMode) {
      print('Speech recognition error: ${error.errorMsg} - permanent: ${error.permanent}');
    }
    _isListening = false;
  }

  /// Callback for handling status changes from the speech recognition engine.
  void _onStatus(String status) {
    if (kDebugMode) {
      print('Speech recognition status: $status');
    }
    _isListening = _speechToText.isListening;
  }
}