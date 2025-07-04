part of 'connectivity_bloc.dart';

abstract class ConnectivityState extends Equatable {
  const ConnectivityState();
  
  @override
  List<Object> get props => [];
}

/// The initial state before the first connectivity check.
class ConnectivityInitial extends ConnectivityState {}

/// The state indicating the device is connected to a network.
class ConnectivityOnline extends ConnectivityState {}

/// The state indicating the device is not connected to any network.
class ConnectivityOffline extends ConnectivityState {}