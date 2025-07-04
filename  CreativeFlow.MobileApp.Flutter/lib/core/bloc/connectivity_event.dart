part of 'connectivity_bloc.dart';

abstract class ConnectivityEvent extends Equatable {
  const ConnectivityEvent();

  @override
  List<Object> get props => [];
}

/// An internal event dispatched when the connectivity status changes.
class _ConnectivityChanged extends ConnectivityEvent {
  final List<ConnectivityResult> result;

  const _ConnectivityChanged(this.result);

  @override
  List<Object> get props => [result];
}

/// An event to manually trigger a connectivity check.
class ConnectivityCheckRequested extends ConnectivityEvent {}