FROM lambci/lambda:build-python3.6

RUN rm /var/runtime/awslambda/runtime.cpython-36m-x86_64-linux-gnu.so && \
	pip install boto3 python-dateutil six && \
	mkdir -p /data 
COPY awslambda/* /var/runtime/awslambda/

# Uncomment this for sys.path debugging
#COPY src/awslambda/bootstrap.py /var/runtime/awslambda/bootstrap.py

USER sbx_user1051

# You have to unset PYTHONPATH here because it is set as an ENV in
# lambdaci/build-python3.6.  If you don't unset it, bootstrap.py decides that
# it doesn't need to set any of the usual Lambda sys.path entries, like
# /var/task and /opt/python
ENTRYPOINT ["/usr/bin/env", "-u", "PYTHONPATH", "/var/lang/bin/python3.6", "/var/runtime/awslambda/bootstrap.py"]
