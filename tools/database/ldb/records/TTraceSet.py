
import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class TTraceSet(Base):
    """
    Describes a single trace set from which statistic traces
    are derived.

    Points to a TraceSetBlob object containing the actual traces.
    """
    
    __tablename__ = "ttracesets"

    id           = Column(Integer,nullable=False,primary_key=True)
    experimentId = Column(Integer,ForeignKey("experiments.id"),nullable=False)
    targetId     = Column(Integer,ForeignKey("targets.id"),nullable=False)
    fixedBlobId  = Column(Integer,ForeignKey("traceset_blobs.id"),nullable=False)
    randomBlobId = Column(Integer,ForeignKey("traceset_blobs.id"),nullable=False)
    ttraceId     = Column(Integer,ForeignKey("statistic_traces.id"))

    tStatisticTrace = relationship("StatisticTrace",
        foreign_keys = ttraceId,
        single_parent= True,
        cascade      = "all, delete-orphan"
    )

    fixedTraceSet = relationship("TraceSetBlob",
        foreign_keys    = fixedBlobId,
        single_parent   = True,
        cascade         = "all, delete-orphan"
    )

    randomTraceSet= relationship("TraceSetBlob",
        foreign_keys    = randomBlobId,
        single_parent   = True,
        cascade         = "all, delete-orphan"
    )

    timestamp    = Column(DateTime, default=datetime.datetime.now)
    parameters   = Column(String, default="")

    def __repr__(self):
        return "%5d, %-16s, %5d, %5d, %5d, %5d, %-40s" % (
            self.id,
            self.timestamp,
            self.experimentId,
            self.targetId,
            self.fixedBlobId,
            self.randomBlobId,
            self.parameters.rstrip("}").lstrip("{")
        )
