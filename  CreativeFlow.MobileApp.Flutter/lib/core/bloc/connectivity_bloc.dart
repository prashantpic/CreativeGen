import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:equatable/equatable.dart';

part 'connectivity_event.dart';
part 'connectivity_state.dart';

/// A BLoC that monitors network connectivity status and emits states
/// indicating whether the device is online or offline.
///
/// Used by UI elements (e.g., [OfflineBanner]) and services (e.g., [SyncService])
/// to react to changes in network availability.
class ConnectivityBloc extends Bloc<ConnectivityEvent, ConnectivityState> {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<List<ConnectivityResult>>? _subscription;

  ConnectivityBloc() : super(ConnectivityInitial()) {
    on<_ConnectivityChanged>(_onConnectivityChanged);
    on<ConnectivityCheckRequested>(_onConnectivityCheckRequested);

    // Subscribe to connectivity changes as soon as the BLoC is created.
    _subscription = _connectivity.onConnectivityChanged.listen((result) {
      add(_ConnectivityChanged(result));
    });
  }

  Future<void> _onConnectivityCheckRequested(
    ConnectivityCheckRequested event,
    Emitter<ConnectivityState> emit,
  ) async {
    // Perform an initial check when requested.
    final result = await _connectivity.checkConnectivity();
    add(_ConnectivityChanged(result));
  }

  void _onConnectivityChanged(
    _ConnectivityChanged event,
    Emitter<ConnectivityState> emit,
  ) {
    if (event.result.contains(ConnectivityResult.none)) {
      // If the result list contains 'none', the device is offline.
      if (state is! ConnectivityOffline) {
        emit(ConnectivityOffline());
      }
    } else {
      // Otherwise, the device has some form of connectivity (Wi-Fi, mobile, etc.).
      if (state is! ConnectivityOnline) {
        emit(ConnectivityOnline());
      }
    }
  }

  @override
  Future<void> close() {
    _subscription?.cancel();
    return super.close();
  }
}