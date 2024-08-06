# MyPackage

This is a simple Python package.


A classic problem in every data replication activity is to make the software detect changes in the source datasets and drive replication activities when a change is detected. 

For that purpose we have constructed a separate daemon process that polls continuously the data sources, based on its knowledge for the replication rules and jobs. In the case of CDH/CDP it was literally a multithreaded daemon that was combing over HDFS.

Could we 

In the case of a local filesystem, we could leverage 

Due to the nature of the data change detection mechanism, we wanted to split the data replication rules into "priority queues". More important data or data that we know change more rapidly, are grouped into higher priority queues, pretty much like (speedy boarding in low-cost airlines!). Less critical data are grouped in lower priority queues, and they're scanned for changes less frequently.

