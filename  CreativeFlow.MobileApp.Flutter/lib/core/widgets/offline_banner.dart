import 'package:creativeflow_mobileapp_flutter/core/bloc/connectivity_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

/// A reusable widget that displays a banner to indicate when the application
/// is offline, as required by UI-004.
///
/// It listens to the [ConnectivityBloc] and shows or hides itself based on
/// the network status.
class OfflineBanner extends StatelessWidget {
  const OfflineBanner({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ConnectivityBloc, ConnectivityState>(
      builder: (context, state) {
        if (state is ConnectivityOffline) {
          // When offline, display the banner.
          return Align(
            alignment: Alignment.topCenter,
            child: Material(
              // The Material widget provides elevation and a background.
              elevation: 4.0,
              child: Container(
                width: double.infinity,
                color: Colors.grey.shade700,
                padding: EdgeInsets.only(
                  top: MediaQuery.of(context).padding.top + 8.0, // Respect status bar
                  bottom: 8.0,
                  left: 16.0,
                  right: 16.0,
                ),
                child: const Center(
                  child: Text(
                    'You are offline',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                    // Ensure the banner text is accessible to screen readers.
                    semanticsLabel: 'Offline status indicator: You are currently offline.',
                  ),
                ),
              ),
            ),
          );
        } else {
          // When online or in initial state, render nothing.
          return const SizedBox.shrink();
        }
      },
    );
  }
}