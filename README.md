[![Build Status](https://travis-ci.org/excamera/pipeline.svg?branch=master)](https://travis-ci.org/excamera/pipeline)

# Video Processing Pipeline (WIP)
This is a Top-Level Project implementing pipelines. This project internally
uses https://github.com/excamera/mu for interacting with mu.

## How to build the code
```
git clone --recursive https://github.com/excamera/pipeline.git
cd pipeline
./autogen.sh
./configure
make -j$(nproc)

cd sprocket/platform/aws_lambda
./autogen.sh
./configure
make -j$(nproc)
```

steps to run the grayscale example:
```
# build Sprocket
./autogen.sh
./configure
make

# then build the lambda launcher
cd sprocket/platform/aws_lambda
./autogen.sh
./configure
make
cd -

# cd to sprocket/platform/aws_lambda

# you can run bin/create_function.sh to create lambda functions
# you’ll need to provide the application’s directory as parameter
# e.g., ffmpeg is there in the sample_app directory


# first we need to set the configs
# modify pipeline_conf.json
# most likely you'll only need to change:
# 	daemon_addr to your local ip (you’ll need a public ip)
#	the paths to your aws keys, and server_cert/server_key files
#      your s3 buckets for storage_base and temp_storage_base. you’ll need proper AWS role that has access to your s3
#      default_lambda_function: the name of the lambda function created with create_function.sh

#  then start the daemon
python pipeline_daemon.py &

# and run the demo grayscale pipeline on Sintel trailer (or any youtube video)
python pipeline_runner.py pipespec/parlink_grayscale.pipe "input_0:video_link:https://www.youtube.com/watch?v=ac7KhViaVqc"

# that's it! you are running a serverless video pipeline!
# note we create one worker for every second of video, so try not to input a very long video 
# because that can exceed the concurrency limit of Lambda
```
