#!/bin/bash
set -ex

TEST_DIRS=tests
DOCKER_AMS_TAG="ams:latest"
export TESTS_SUFFIX="bin"
export PORTS_PREFIX="92 57"

. .venv-jenkins/bin/activate

docker pull clearlinux
make DOCKER_AMS_TAG=${DOCKER_AMS_TAG} docker_build_ams dldt_package_url=${OPENVINO_DOWNLOAD_LINK_2020_3}
make DOCKER_AMS_TAG=${DOCKER_AMS_TAG}-clearlinux docker_build_ams_clearlinux dldt_package_url=${OPENVINO_DOWNLOAD_LINK_2020_3}

NO_PROXY=localhost py.test ${TEST_DIRS}/functional/test_single_model_vehicle_attributes.py \
                           ${TEST_DIRS}/functional/test_ams_inference.py \
                           -v --test_dir=/var/jenkins_home/test_ovms_models-${TESTS_SUFFIX} \
                           --image ${DOCKER_AMS_TAG}

NO_PROXY=localhost py.test ${TEST_DIRS}/functional/test_single_model_vehicle_attributes.py \
                           ${TEST_DIRS}/functional/test_ams_inference.py \
                           -v --test_dir=/var/jenkins_home/test_ovms_models-${TESTS_SUFFIX} \
                           --image ${DOCKER_AMS_TAG}-clearlinux

NO_PROXY=localhost py.test ${TEST_DIRS}/functional/test_single_model_vehicle_attributes.py \
                           ${TEST_DIRS}/functional/test_ams_inference.py \
                           -v --test_dir=/var/jenkins_home/test_ovms_models-${TESTS_SUFFIX} \
                           --image ${DOCKER_AMS_TAG}

NO_PROXY=localhost py.test ${TEST_DIRS}/functional/test_single_model_vehicle_attributes.py \
                           ${TEST_DIRS}/functional/test_ams_inference.py \
                           -v --test_dir=/var/jenkins_home/test_ovms_models-${TESTS_SUFFIX} \
                           --image ${DOCKER_AMS_TAG}-clearlinux