from pyspark.sql import DataFrame, SQLContext
from pyspark.sql.functions import array, lit, struct

from prophecy.config import ConfigBase


def typed_lit(obj):
    if isinstance(obj, list):
        return array([typed_lit(x) for x in obj])
    elif isinstance(obj, dict):
        elementsList = []
        for key, value in obj.items():
            elementsList.append(typed_lit(value).alias(key))
        return struct(elementsList)
    elif isinstance(obj, ConfigBase.SecretValue):
        return lit(str(obj))
    else:
        try:
            # int, float, string
            return lit(obj)
        except:
            # class type
            return typed_lit(obj.__dict__)


def has_column(df, col):
    try:
        df[col]
        return True
    except:
        return False


def createScalaList(spark, l):
    return spark.sparkContext._jvm.PythonUtils.toList(l)


def createScalaColumnList(spark, cols):
    return spark.sparkContext._jvm.PythonUtils.toList([item._jc for item in list(cols)])


def createScalaMap(spark, dict):
    return spark.sparkContext._jvm.PythonUtils.toScalaMap(dict)


def createScalaColumnMap(spark, dict):
    jcolDict = {k: col._jc for k, col in dict.items()}
    return spark.sparkContext._jvm.PythonUtils.toScalaMap(jcolDict)


def createScalaColumnOption(spark, value):
    if value is None:
        return spark.sparkContext._jvm.scala.Option.apply(None)
    else:
        return spark.sparkContext._jvm.scala.Some(value._jc)


def createScalaOption(spark, value):
    if value is None:
        return spark.sparkContext._jvm.scala.Option.apply(None)
    else:
        return spark.sparkContext._jvm.scala.Some(value)


def isBlank(myString):
    if isinstance(myString, str) and myString and myString.strip():
        return False
    return True


def directory_listing(spark, directory_path, recursive, pattern):
    df_java = spark.sparkContext._jvm.io.prophecy.abinitio.ScalaFunctions._directory_listing_v2(spark._jsparkSession,
                                                                                           directory_path, recursive,
                                                                                           pattern)
    return DataFrame(df_java, SQLContext(spark.sparkContext, sparkSession=spark))


def filter_columns_by_expr(spark, df, expr):
    df_java = spark.sparkContext._jvm.io.prophecy.abinitio.ScalaFunctions.filterColumnsByExpr(
        spark._jsparkSession, df._jdf, expr
    )
    return DataFrame(df_java, SQLContext(spark.sparkContext, sparkSession=spark))

def filter_columns_by_type(spark, df, types):
    types_java = spark._jvm.java.util.ArrayList()
    for t in types:
        types_java.add(t)
    df_java = spark.sparkContext._jvm.io.prophecy.abinitio.ScalaFunctions.filterColumnsByType(
        spark._jsparkSession, df._jdf, types_java
    )
    return DataFrame(df_java, SQLContext(spark.sparkContext, sparkSession=spark))
