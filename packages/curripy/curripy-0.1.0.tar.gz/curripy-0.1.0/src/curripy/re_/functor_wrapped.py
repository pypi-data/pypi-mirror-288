from returns.maybe import maybe
import re
from . import search

searchWrapped = maybe(re.search)
searchWrapped_ = maybe(search)
