import logging
from opentelemetry import trace, _logs
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# 1. 設定 Traces 管道
trace_provider = TracerProvider()
trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer("o.demo")

# 2. 設定 Logs 管道
logger_provider = LoggerProvider()
log_exporter = OTLPLogExporter(endpoint="http://localhost:4317")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
_logs.set_logger_provider(logger_provider)

# 綁定標準 logging
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger("o.demo.logger")

# 3. 執行業務邏輯並送出資料
with tracer.start_as_current_span("multi-pipeline-checkout"):
    logger.info("User initiated checkout process with multi-pipeline.")
    with tracer.start_as_current_span("charge-card"):
        logger.info("Card charged successfully via OTLP logs.")
        print("Traces and Logs sent to multi-pipeline collector!")