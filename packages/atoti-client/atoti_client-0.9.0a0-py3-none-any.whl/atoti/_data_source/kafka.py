from __future__ import annotations

from collections.abc import Mapping
from datetime import timedelta
from typing import final

from typing_extensions import override

from .._identification import TableIdentifier
from .data_source import DataSource


@final
class KafkaDataSource(DataSource):
    @property
    @override
    def key(self) -> str:
        return "KAFKA"

    def load_kafka_into_table(
        self,
        identifier: TableIdentifier,
        *,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        batch_duration: timedelta,
        consumer_config: Mapping[str, str],
        scenario_name: str | None,
    ) -> None:
        """Consume a Kafka topic and stream its records in an existing table."""
        params: dict[str, object] = {
            "bootstrapServers": bootstrap_servers,
            "topic": topic,
            "consumerGroupId": group_id,
            "keyDeserializerClass": "org.apache.kafka.common.serialization.StringDeserializer",
            "batchDuration": int(batch_duration.total_seconds() * 1000),
            "additionalParameters": consumer_config,
        }
        self.load_data_into_table(
            identifier,
            params,
            scenario_name=scenario_name,
        )
