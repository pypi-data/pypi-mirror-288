#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of WriteBaseTransformer is responsible for writing Stream objects
"""
import logging
import typing
import zlib

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.write.transformer import Transformer
from borb.io.write.transformer import WriteTransformerState

logger = logging.getLogger(__name__)


class StreamTransformer(Transformer):
    """
    This implementation of WriteBaseTransformer is responsible for writing Stream objects
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def can_be_transformed(self, object: AnyPDFType):
        """
        This function returns True if the object to be transformed is a Stream
        :param object:  the object to be transformed
        :return:        True if the object is a Stream, False otherwise
        """
        return isinstance(object, Stream)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: typing.Optional[WriteTransformerState] = None,
    ):
        """
        This function transforms a Stream into a byte stream
        :param object_to_transform:     the Stream to transform
        :param context:                 the WriteTransformerState (containing passwords, etc)
        :return:                        a (serialized) Stream
        """
        # fmt: off
        assert (context is not None), "context must be defined in order to write Stream objects."
        assert context.destination is not None, "context.destination must be defined in order to write Stream objects."
        assert isinstance(object_to_transform, Stream), "object_to_transform must be of type Stream"
        # fmt: on

        # avoid resolving objects twice
        object_ref: typing.Optional[Reference] = object_to_transform.get_reference()
        if object_ref is not None and object_ref in context.resolved_references:
            assert object_ref is not None
            assert object_ref.object_number is not None
            logger.debug(
                "skip writing object %d %d R (already resolved)"
                % (object_ref.object_number, object_ref.generation_number or 0)
            )
            return

        # start object if needed
        started_object = False
        if object_ref is not None:
            assert object_ref.object_number is not None
            if object_ref.object_number is not None and object_ref.byte_offset is None:
                started_object = True
                self._start_object(object_to_transform, context)
            context.resolved_references.append(object_ref)

        # build stream dictionary
        stream_dictionary = Dictionary()

        # objects to turn into reference
        queue: typing.List[AnyPDFType] = []
        for k, v in object_to_transform.items():
            if k in ["Bytes", "DecodedBytes"]:
                continue
            if (
                isinstance(v, Dictionary)
                or isinstance(v, List)
                or isinstance(v, Stream)
            ) and not v.is_inline():
                stream_dictionary[k] = self.get_reference(v, context)
                queue.append(v)
            else:
                stream_dictionary[k] = v

        # if self.compression_level == 0, remove /Filter
        if context.compression_level == 0 and Name("Filter") in stream_dictionary:
            stream_dictionary.pop(Name("Filter"))

        # handle compression
        if "DecodedBytes" in object_to_transform:
            if context.compression_level == 0:
                bts = object_to_transform["DecodedBytes"]
            else:
                bts = zlib.compress(
                    object_to_transform["DecodedBytes"], context.compression_level
                )
            stream_dictionary[Name("Length")] = bDecimal(len(bts))
        else:
            assert "Bytes" in object_to_transform
            bts = object_to_transform["Bytes"]

        # write stream dictionary
        self.get_root_transformer().transform(stream_dictionary, context)

        # write "stream"
        context.destination.write(bytes("stream\n", "latin1"))

        # write bytes
        context.destination.write(bts)

        # write "endstream"
        context.destination.write(bytes("\nendstream\n", "latin1"))

        # end object if needed
        if started_object:
            self._end_object(object_to_transform, context)

        for e in queue:
            self.get_root_transformer().transform(e, context)
