# Shared Types

```python
from endex_factset_estimates.types import ConsensusResponse, DetailResponse
```

# FactsetEstimates

## V2

### RollingConsensus

Methods:

- <code title="post /factset-estimates/v2/rolling-consensus">client.factset_estimates.v2.rolling_consensus.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/rolling_consensus.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/rolling_consensus_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/consensus_response.py">ConsensusResponse</a></code>
- <code title="get /factset-estimates/v2/rolling-consensus">client.factset_estimates.v2.rolling_consensus.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/rolling_consensus.py">list</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/rolling_consensus_list_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/consensus_response.py">ConsensusResponse</a></code>

### FixedConsensus

Methods:

- <code title="post /factset-estimates/v2/fixed-consensus">client.factset_estimates.v2.fixed_consensus.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/fixed_consensus.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/fixed_consensus_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/consensus_response.py">ConsensusResponse</a></code>
- <code title="get /factset-estimates/v2/fixed-consensus">client.factset_estimates.v2.fixed_consensus.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/fixed_consensus.py">retrieve</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/fixed_consensus_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/consensus_response.py">ConsensusResponse</a></code>

### RollingDetail

Methods:

- <code title="post /factset-estimates/v2/rolling-detail">client.factset_estimates.v2.rolling_detail.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/rolling_detail.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/rolling_detail_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/detail_response.py">DetailResponse</a></code>
- <code title="get /factset-estimates/v2/rolling-detail">client.factset_estimates.v2.rolling_detail.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/rolling_detail.py">list</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/rolling_detail_list_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/detail_response.py">DetailResponse</a></code>

### FixedDetail

Methods:

- <code title="post /factset-estimates/v2/fixed-detail">client.factset_estimates.v2.fixed_detail.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/fixed_detail.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/fixed_detail_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/detail_response.py">DetailResponse</a></code>
- <code title="get /factset-estimates/v2/fixed-detail">client.factset_estimates.v2.fixed_detail.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/fixed_detail.py">list</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/fixed_detail_list_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/shared/detail_response.py">DetailResponse</a></code>

### ConsensusRatings

Types:

```python
from endex_factset_estimates.types.factset_estimates.v2 import ConsensusRatingsResponse
```

Methods:

- <code title="post /factset-estimates/v2/consensus-ratings">client.factset_estimates.v2.consensus_ratings.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/consensus_ratings.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/consensus_rating_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/consensus_ratings_response.py">ConsensusRatingsResponse</a></code>
- <code title="get /factset-estimates/v2/consensus-ratings">client.factset_estimates.v2.consensus_ratings.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/consensus_ratings.py">list</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/consensus_rating_list_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/consensus_ratings_response.py">ConsensusRatingsResponse</a></code>

### DetailRatings

Types:

```python
from endex_factset_estimates.types.factset_estimates.v2 import DetailRatingsResponse
```

Methods:

- <code title="post /factset-estimates/v2/detail-ratings">client.factset_estimates.v2.detail_ratings.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/detail_ratings.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/detail_rating_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/detail_ratings_response.py">DetailRatingsResponse</a></code>
- <code title="get /factset-estimates/v2/detail-ratings">client.factset_estimates.v2.detail_ratings.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/detail_ratings.py">retrieve</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/detail_rating_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/detail_ratings_response.py">DetailRatingsResponse</a></code>

### Surprise

Types:

```python
from endex_factset_estimates.types.factset_estimates.v2 import SurpriseResponse
```

Methods:

- <code title="post /factset-estimates/v2/surprise">client.factset_estimates.v2.surprise.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/surprise.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/surprise_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/surprise_response.py">SurpriseResponse</a></code>
- <code title="get /factset-estimates/v2/surprise">client.factset_estimates.v2.surprise.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/surprise.py">retrieve</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/surprise_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/surprise_response.py">SurpriseResponse</a></code>

### Segments

Types:

```python
from endex_factset_estimates.types.factset_estimates.v2 import SegmentsResponse
```

Methods:

- <code title="post /factset-estimates/v2/segments">client.factset_estimates.v2.segments.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/segments.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/segment_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/segments_response.py">SegmentsResponse</a></code>
- <code title="get /factset-estimates/v2/segments">client.factset_estimates.v2.segments.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/segments.py">retrieve</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/segment_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/segments_response.py">SegmentsResponse</a></code>

### Metrics

Types:

```python
from endex_factset_estimates.types.factset_estimates.v2 import MetricsResponse
```

Methods:

- <code title="post /factset-estimates/v2/metrics">client.factset_estimates.v2.metrics.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/metrics.py">create</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/metric_create_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/metrics_response.py">MetricsResponse</a></code>
- <code title="get /factset-estimates/v2/metrics">client.factset_estimates.v2.metrics.<a href="./src/endex_factset_estimates/resources/factset_estimates/v2/metrics.py">list</a>(\*\*<a href="src/endex_factset_estimates/types/factset_estimates/v2/metric_list_params.py">params</a>) -> <a href="./src/endex_factset_estimates/types/factset_estimates/v2/metrics_response.py">MetricsResponse</a></code>
