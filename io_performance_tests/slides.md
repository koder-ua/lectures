!SLIDE
### Performance tests topics
    * Introducton
    * HDD/SSD/Ceph/etc difference from performance test POV
    * Test cases selection
    * Test results processing
    * Test results presentation
    * Low-level testing tools (fio)
    * Hight-level testing tools (cbt, cosbench)
    * wally

!SLIDE
### Introduction
    Show some results

!SLIDE
### Issues with test results
    * They (mostly) all different
    * Lack of information (can't compare to local)

!SLIDE
### Three type of tests
    * Real workload
    * Low-level - iops/bw/lat (SPC-1, SPC-2)
    * All other

!SLIDE
### Know you enemy

!SLIDE
### HDD
![](../images/simplified_schema_of_hdd.jpg)

!SLIDE
### How OS + HDD process request
![](../images/linux_io_request_path_OS.png)
+ Caches, requests reordering

!SLIDE
### OS + HDD request process time
#### IO\_TIME = SEEK\_TIME + TRANSFER\_SIZE / BW

!SLIDE
### SSD structure (computer inside computer)
![](../images/ssd_structure.jpg)

!SLIDE
### SSD issues
    * Need large active queue to get more iops
    * Limited write cycles
    * No overwrite
    * TRIM
    * Write amplification

!SLIDE
### SSD other performance issues
    * Write BW over the time
    * Mixed workload issue

!SLIDE
### SSD vs HDD average performance
![](../images/ssd-vs-hdd.jpg)

!SLIDE
### RAID performance

!SLIDE
### Distributed storages

!SLIDE
### Ceph
    * Linear performance depends on queue depth

!SLIDE
### What parameters need to measure - IOPS + Lat
    * IOPS has a meaning only for small blocks
    * IOPS depends on thread count - PLOT
    * Latency depends on thread count - PLOT
    * Storage IOPS is different for different types of load

!SLIDE
### What parameters need to measure - BW
    * Avg lat ~10ms. Avg BW ~200MBps.
    * For blocks, smaller than ~2M latency dominates processing time

!SLIDE
### On what parameters they may depend
    * block size
    * client count
    * operation mode
    * operation r,w,r+w
    * ramp-up time
    * test time

!SLIDE
### Need to select subspace
    * Don't try to guess values, unless you are totaly confident (and you are not)
    * Make a model, check it with several tests. Make some scan on other
    * Select minimal test suite. It must not takes an hours.

#### Examples
    * No r+w workloads for HDD
    * No linear BW tests with 2+ threads

!SLIDE
### Particular technics
    * Prefill storage before test - first write often slower
    * Test with pseudo-random data - bypass comression
    * Always warm-up
    * Record IOPS/BW during test. Check, that they are stail
    * Ceph - disable scrub/deep scrub
    * Always use direct/direct+sync mode, if possible
    * Flush cache before test

!SLIDE 
### Collect usage during tests

!SLIDE
### Postrocessing - deviation
    * 42 is not an answer
    * Calculate deviation
    * (42 +- 5) is not an answer as well
    * Deviation give a probability that particular result would
      fits into some range
    * Large deviation mean that there something wrong with test/system

!SLIDE
### Postrocessing - deviation
![](../images/Standard_deviation_diagram.png)

!SLIDE
### Postrocessing - confidence interval
    * Deviation tell you range where result on any particular test should be
    * Confidence interval tell you range where "real" value should be

~~~~{python}
    from scipy import stats
    confidence = stats.sem(data) * \
        stats.t.ppf((1 + confidence) / 2, ln - 1)
~~~~

!SLIDE
### But only for normal distribution
    * Does (mediana == average)
    * IOPS & BW usually distributed normally
    * Latency never distributed normally
    * So we have to "show" distribution using percentiles

![](../images/q3-latency-f1.gif)

!SLIDE
### Why we are showing plots?

!SLIDE
### Test results presentation
    * Always show deviation
    * No large tables
    * Plot dependent data on same graph
    * Collect parameters of you cluster
    * ceph-monitoring (https://github.com/koder-ua/ceph-monitoring)
    * Log-scale plots

!SLIDE
### Testing tools (low-level)
    * iobench, bonnie++,.... - over 8000
    * fio is the tool

!SLIDE
### fio
~~~~
[global]
group_reporting
wait_for_previous
ramp_time=0
filename=${FILENAME}
buffered=0
iodepth=1
size=1000m
time_based

[writetest]
blocksize=4k
rw=randwrite
direct=1
runtime=30
numjobs=1

[readtest]
numjobs=4
blocksize=4k
rw=randread
direct=1
runtime=30
~~~~

!SLIDE
### fio
~~~~
fio --output-format=json --output=XXX --alloc-size=262144 {job_file} >{err_out_file} 2>&1
~~~~

!SLIDE
### fio
~~~~
write_lat_log=fio_log
write_iops_log=fio_log
write_bw_log=fio_log
log_avg_msec=500
~~~~

!SLIDE
### cbt
    * https://github.com/ceph/cbt

!SLIDE
### rally


!SLIDE
###

!SLIDE
### wally
    * https://github.com/Mirantis/disk_perf_test_tool
    * Block disk storage tests, DB test(TCP-B), SCP
    * Runs fio internally
    * Cooperate with openstack and FUEL
    * Run test in parallel from several nodes
    * Can spawn VM on openstack, reuse existing VM or hosts
    * Comprehencite test suits for main storages

!SLIDE
### wally workflow
    * Detect given clusters (FUEL/OS/Ceph)
    * Spawn test nodes on OS, if needed
    * Connect to test nodes
    * Run fio test
    * Make report

!SLIDE
### wally config part 1
~~~~{yaml}
include: default.yaml
lab_name: perf-3

clouds:
    fuel:
        url: "http://172.16.52.114:8000/"
        creds: "admin:admin@admin"
        ssh_creds: "root:root_passwd"
        openstack_env: "SaharaMurano"
    # openstack:
        # OPENRC: /var/wally_results/uncartooned_barbara/results/SaharaMurano_openrc
        # vms:
        #     - "ubuntu@wally-uncartooned_barbara"

discover: fuel_openrc_only
~~~~

!SLIDE
### wally config part 2
~~~~{yaml}

# explicit_nodes:
#    "ssh://root@localhost:7777:/home/koder/.ssh/fuel_master_ceph_rsa": testnode

# sensors:
#     roles_mapping:
#         testnode: system-cpu, block-io, net-io
#         compute: system-cpu, block-io, net-io

tests:
  - start_test_nodes:
        openstack:
            count: =2
            cfg_name: wally_1024
            network_zone_name: admin_internal_net
            flt_ip_pool: admin_floating_net

        tests:
          - io:
                cfg: ceph  # --> wally/suits/io/ceph.cfg
                params:
                    FILENAME: /dev/vdb
                    TEST_FILE_SIZE: 30G
~~~~

!SLIDE
### wally run
~~~~
$ export PYTHONPATH=/home/koder/workspace/wally
$ python -m wally test "just a test" ~/.wally_loads/local.yaml
~~~~

!SLIDE
###
~~~~
~~~~

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

!SLIDE
###

    