import 'package:flutter/foundation.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_result.dart';

/// An abstraction layer over the native speech-to-text plugin.
///
/// This service provides a clean interface for using the device's speech
/// recognition capabilities, abstracting the complexities of the underlying
/// `speech_to_text` plugin and making features that use it easier to test.
abstract class VoiceRecognitionService {
  /// Initializes the speech recognizer.
  ///
  /// Must be called once before `startListening`. Returns `true` if
  /// initialization is successful.
  Future<bool> initialize();

  /// Starts a listening session for speech recognition.
  ///
  /// The [onResult] callback is invoked with the transcribed text as the
  /// user speaks.
  void startListening({required Function(String) onResult});

  /// Stops the current listening session.
  void stopListening();

  /// Returns `true` if the service is currently listening for speech.
  bool get isListening;
}

/// The concrete implementation of [VoiceRecognitionService] using the
/// `speech_to_text` package.
class VoiceRecognitionServiceImpl implements VoiceRecognitionService {
  final SpeechToText _speechToText;
  bool _isInitialized = false;

  // Allows injecting a mock for testing.
  VoiceRecognitionServiceImpl({SpeechToText? speechToText}) 
    : _speechToText = speechToText ?? SpeechToText();

  @override
  Future<bool> initialize() async {
    if (_isInitialized) return true;

    try {
      _isInitialized = await _speechToText.initialize(
        onError: (error) => debugPrint('Speech recognition error: $error'),
        onStatus: (status) => debugPrint('Speech recognition status: $status'),
      );
    } catch (e) {
      debugPrint('Exception during speech initialization: $e');
      _isInitialized = false;
    }
    
    return _isInitialized;
  }

  @override
  bool get isListening => _speechToText.isListening;

  @override
  void startListening({required Function(String) onResult}) {
    if (!_isInitialized || isListening) {
      debugPrint('Cannot start listening. Initialized: $_isInitialized, Is Listening: $isListening');
      return;
    }
    
    _speechToText.listen(
      onResult: (SpeechRecognitionResult result) {
        onResult(result.recognizedWords);
      },
      // You can configure other parameters like localeId, listenMode, etc.
      // localeId: 'en_US',
    );
  }

  @override
  void stopListening() {
    if (!_isInitialized || !isListening) {
      debugPrint('Cannot stop listening. Not initialized or not listening.');
      return;
    }
    
    _speechToText.stop();
  }
}