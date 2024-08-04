from .aggregate import AggregatorFeed
from .collect import CollectorFeed
from .csvfeed import CSVFeed
from .eventchannel import EventChannel
from .feed import Feed
from .historic import HistoricFeed
from .randomwalk import RandomWalk
from .sqllitefeed import SQLFeed
from .parquetfeed import ParquetFeed
from .avrofeed import AvroFeed

try:
    from .yahoo import YahooFeed
except ImportError:
    pass
