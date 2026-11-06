import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node album
album_node1750957376579 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-datapipeline/staging/albums.csv"], "recurse": True}, transformation_ctx="album_node1750957376579")

# Script generated for node tracks
tracks_node1750957377511 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-datapipeline/staging/track.csv"], "recurse": True}, transformation_ctx="tracks_node1750957377511")

# Script generated for node artist
artist_node1750957377040 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://project-datapipeline/staging/artists.csv"], "recurse": True}, transformation_ctx="artist_node1750957377040")

# Script generated for node Join Album and Artist
JoinAlbumandArtist_node1750957523127 = Join.apply(frame1=album_node1750957376579, frame2=artist_node1750957377040, keys1=["artist_id"], keys2=["id"], transformation_ctx="JoinAlbumandArtist_node1750957523127")

# Script generated for node Join
Join_node1750957707406 = Join.apply(frame1=tracks_node1750957377511, frame2=JoinAlbumandArtist_node1750957523127, keys1=["track_id"], keys2=["track_id"], transformation_ctx="Join_node1750957707406")

# Script generated for node Drop Fields
DropFields_node1750957894420 = DropFields.apply(frame=Join_node1750957707406, paths=["`.track_id`", "id"], transformation_ctx="DropFields_node1750957894420")

# Script generated for node Destination
EvaluateDataQuality().process_rows(frame=DropFields_node1750957894420, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1750956703754", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Destination_node1750957978378 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1750957894420, connection_type="s3", format="glueparquet", connection_options={"path": "s3://project-datapipeline/datawarehouse/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="Destination_node1750957978378")

job.commit()