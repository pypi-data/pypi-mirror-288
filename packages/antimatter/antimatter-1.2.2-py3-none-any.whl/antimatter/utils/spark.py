# This file contains helpers for spark to register udfs for encapsulation and loading capsule given the spark session
# and the antimatter session

import base64

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from antimatter.errors import MissingDependency
from antimatter.session import EncapsulateResponse, Session


def register_pyspark_udfs(
    spark: SparkSession, sess: Session, read_context="default", write_context="sensitive"
) -> None:
    try:
        from pyspark.sql.types import (
            StringType,
            IntegerType,
            FloatType,
            BooleanType,
            ByteType,
            DateType,
            TimestampType,
            LongType,
            DoubleType,
        )
    except ImportError:
        raise MissingDependency("pyspark not found, please install pyspark to register spark udfs")

    def _base64_enc(data: EncapsulateResponse):
        return base64.b64encode(data.raw).decode()

    def _base64_dec(data: str):
        return base64.b64decode(data)

    def _encapsulate_helper(data, write_context=write_context):
        capsule = sess.encapsulate(data, write_context=write_context)
        return _base64_enc(capsule)

    def _load_capsule_helper(data, read_context=read_context):
        capsule = sess.load_capsule(data=_base64_dec(data), read_context=read_context)
        return capsule.data()

    def _classify_and_redact_helper(data, read_context=read_context, write_context=write_context):
        return sess.classify_and_redact(data, read_context=read_context, write_context=write_context).data()

    data_types = [
        ("str", StringType),
        ("int", IntegerType),
        ("float", FloatType),
        ("bool", BooleanType),
        ("byte", ByteType),
        ("date", DateType),
        ("timestamp", TimestampType),
        ("long", LongType),
        ("double", DoubleType),
    ]
    for type_name, spark_type in data_types:
        encapsulate_udf = udf(_encapsulate_helper, spark_type())
        load_capsule_udf = udf(_load_capsule_helper, spark_type())
        classify_and_redact_udf = udf(_classify_and_redact_helper, spark_type())

        spark.udf.register(f"encapsulate_{type_name}", encapsulate_udf)
        spark.udf.register(f"load_capsule_{type_name}", load_capsule_udf)
        spark.udf.register(f"classify_and_redact_{type_name}", classify_and_redact_udf)
