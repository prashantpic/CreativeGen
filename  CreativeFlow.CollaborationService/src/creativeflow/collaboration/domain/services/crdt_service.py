from typing import List

import y_py as ypy
from y_py import YDoc


class CrdtService:
    """
    Domain service for CRDT operations, abstracting y-py library specifics.
    This service provides a higher-level, stateless interface for interacting with
    the Yjs (y-py) library for CRDT operations. It wraps core y-py functionalities
    to ensure consistent usage across the application.
    """

    @staticmethod
    def initialize_document() -> YDoc:
        """
        Creates and returns a new, empty YDoc.

        Returns:
            YDoc: A new Yjs document instance.
        """
        return YDoc()

    @staticmethod
    def apply_update_to_document(ydoc: YDoc, update_payload: bytes) -> None:
        """
        Applies a binary update to a YDoc.

        This is used to incorporate changes from other clients into the local
        document state.

        Args:
            ydoc (YDoc): The Yjs document to update.
            update_payload (bytes): The binary update payload received from another client.
        """
        ypy.apply_update(ydoc, update_payload)

    @staticmethod
    def encode_state_vector(ydoc: YDoc) -> bytes:
        """
        Encodes the state vector of a YDoc.

        The state vector represents the versions of all updates known to the YDoc
        and is used by other clients to compute the minimal differential update (diff).

        Args:
            ydoc (YDoc): The Yjs document.

        Returns:
            bytes: The encoded state vector.
        """
        return ypy.encode_state_vector(ydoc)

    @staticmethod
    def encode_state_as_update(ydoc: YDoc, encoded_target_state_vector: bytes = None) -> bytes:
        """
        Encodes the YDoc's state as a binary update.

        If a target state vector is provided, it computes a differential update (diff)
        containing only the changes not present in the target state. If no target state
        vector is provided, it encodes the entire document state as an update.

        Args:
            ydoc (YDoc): The Yjs document to encode.
            encoded_target_state_vector (bytes, optional): The state vector of the
                remote client requesting the update. Defaults to None.

        Returns:
            bytes: The binary update payload (either a full update or a diff).
        """
        return ypy.encode_state_as_update(ydoc, encoded_target_state_vector)

    @staticmethod
    def merge_updates(ydoc: YDoc, updates: List[bytes]) -> None:
        """
        Merges a list of updates into a YDoc.

        This is useful for applying a batch of updates, for instance, when
        merging offline changes.

        Args:
            ydoc (YDoc): The Yjs document to merge updates into.
            updates (List[bytes]): A list of binary update payloads.
        """
        # y-py does not have a direct `merge_updates` function like some Yjs libraries.
        # The standard approach is to apply them sequentially.
        # A transaction ensures atomicity for the batch operation.
        with ydoc.begin_transaction() as txn:
            for update in updates:
                ypy.apply_update(ydoc, update, txn)