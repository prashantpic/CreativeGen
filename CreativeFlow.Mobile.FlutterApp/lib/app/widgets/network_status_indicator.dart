import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';

/// A global UI widget that persistently displays the current network
/// connectivity status (online/offline) to the user.
///
/// It listens to network changes and shows a non-intrusive banner when the
/// device is offline, providing clear and constant feedback.
class NetworkStatusIndicator extends StatefulWidget {
  final Widget child;

  /// Wraps the given [child] widget with the network status indicator functionality.
  const NetworkStatusIndicator({super.key, required this.child});

  @override
  State<NetworkStatusIndicator> createState() => _NetworkStatusIndicatorState();
}

class _NetworkStatusIndicatorState extends State<NetworkStatusIndicator> {
  late final StreamSubscription<List<ConnectivityResult>> _connectivitySubscription;
  bool _isOffline = false;

  @override
  void initState() {
    super.initState();
    _checkInitialConnectivity();
    _connectivitySubscription =
        Connectivity().onConnectivityChanged.listen(_updateConnectionStatus);
  }

  @override
  void dispose() {
    _connectivitySubscription.cancel();
    super.dispose();
  }

  Future<void> _checkInitialConnectivity() async {
    final result = await Connectivity().checkConnectivity();
    _updateConnectionStatus(result);
  }

  void _updateConnectionStatus(List<ConnectivityResult> result) {
    setState(() {
      _isOffline = result.contains(ConnectivityResult.none);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        widget.child,
        if (_isOffline)
          const Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: _OfflineBanner(),
          ),
      ],
    );
  }
}

class _OfflineBanner extends StatelessWidget {
  const _OfflineBanner();

  @override
  Widget build(BuildContext context) {
    return Material(
      // Use Material to ensure text styles are applied correctly.
      color: Colors.transparent,
      child: Container(
        color: Colors.black87,
        padding: EdgeInsets.fromLTRB(
          12.0,
          8.0,
          12.0,
          8.0 + MediaQuery.of(context).padding.bottom, // Respect safe area
        ),
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.wifi_off, color: Colors.white, size: 16),
            SizedBox(width: 8),
            Text(
              'Offline Mode',
              style: TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}